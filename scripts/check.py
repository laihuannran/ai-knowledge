"""Validate content references and the emitted site, without network dependencies."""
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

from catalog import ROOT, load_articles
from edition import read_json

D = ROOT / 'dist'
ARTICLES = load_articles()
errors = []


class Doc(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.cards = 0
        self.term_entries = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:
                errors.append(f'Duplicate HTML id: {a["id"]}')
            self.ids.add(a['id'])
        for key in ('href', 'src'):
            if a.get(key):
                self.links.append(a[key])
        if tag == 'img' and not a.get('alt'):
            errors.append('Image without alt')
        if 'article-card' in a.get('class', '').split():
            self.cards += 1
        if 'data-term' in a:
            self.term_entries += 1


slugs = set()
for a in ARTICLES:
    slug = a['slug']
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        errors.append(f'Unsafe slug: {slug}')
    if slug in slugs:
        errors.append(f'Duplicate slug: {slug}')
    slugs.add(slug)
    for field in ('title', 'category', 'summary', 'analogy', 'nodes', 'sections', 'example',
                  'pitfall', 'question', 'answer', 'sources', 'tags', 'requires', 'date'):
        if not a.get(field):
            errors.append(f'Missing {field}: {slug}')
    if len(a['nodes']) != 4:
        errors.append(f'Expected four diagram nodes: {slug}')
    if len(a['sections']) < 3:
        errors.append(f'Insufficient explanation: {slug}')
    for source in a['sources']:
        if not source['url'].startswith('https://') or not source['title']:
            errors.append(f'Invalid source: {slug}')
    if a.get('diagram_type', 'flow') not in {'flow', 'comparison', 'branch', 'cycle', 'timeline'}:
        errors.append(f'Unknown diagram type: {slug}')
    table = a.get('comparison')
    if table:
        if len(table['headers']) < 2 or not table['rows']:
            errors.append(f'Invalid comparison: {slug}')
        if any(len(row) != len(table['headers']) for row in table['rows']):
            errors.append(f'Ragged table: {slug}')
    markdown = ROOT / 'content' / f'{slug}.md'
    if not markdown.exists():
        errors.append(f'Missing Markdown: {slug}')
    else:
        text = markdown.read_text()
        for section in a['sections']:
            if section['text'] not in text:
                errors.append(f'Markdown lost explanation: {slug}')

for a in ARTICLES:
    for field in ('prerequisites', 'related'):
        for target in a.get(field, []):
            if target not in slugs or target == a['slug']:
                errors.append(f'Invalid {field} target: {a["slug"]} -> {target}')

# A prerequisite cycle gives readers no starting point; related links may cycle.
by_slug = {a['slug']: a for a in ARTICLES}
visited, active = set(), set()
def visit(slug):
    if slug in active:
        errors.append(f'Prerequisite cycle at {slug}')
        return
    if slug in visited or slug not in by_slug:
        return
    active.add(slug)
    for target in by_slug[slug].get('prerequisites', []):
        visit(target)
    active.remove(slug)
    visited.add(slug)
for slug in slugs:
    visit(slug)

docs = {}
for path in D.rglob('*.html'):
    doc = Doc()
    doc.feed(path.read_text())
    docs[path.resolve()] = doc
for path, doc in docs.items():
    for link in doc.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if not target.is_relative_to(D.resolve()):
            errors.append(f'Escapes site: {path}: {link}')
        elif not target.exists():
            errors.append(f'Broken link: {path}: {link}')
        elif url.fragment and target in docs and unquote(url.fragment) not in docs[target].ids:
            errors.append(f'Broken fragment: {path}: {link}')

# Repository readers use the Markdown edition, including its relative SVG paths.
for article in ARTICLES:
    path = ROOT / 'content' / f'{article["slug"]}.md'
    if not path.exists():
        continue
    for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', path.read_text()):
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if not target.is_relative_to(ROOT.resolve()):
            errors.append(f'Markdown escapes repository: {path}: {link}')
        elif not target.exists():
            errors.append(f'Broken Markdown path: {path}: {link}')
        elif url.fragment:
            if target in docs:
                anchors = docs[target].ids
            elif target.suffix == '.md':
                headings = re.findall(r'^#{1,6}\s+(.+)$', target.read_text(), re.MULTILINE)
                anchors = {re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-') for h in headings}
            else:
                anchors = set()
            if unquote(url.fragment) not in anchors:
                errors.append(f'Broken Markdown fragment: {path}: {link}')

svg_paths = list((D / 'diagrams').glob('*.svg'))
for path in svg_paths:
    root = ET.parse(path).getroot()
    ns = {'s': 'http://www.w3.org/2000/svg'}
    if root.find('s:title', ns) is None or root.find('s:desc', ns) is None:
        errors.append(f'Missing accessible diagram description: {path}')
expected_diagrams = sum(1 + len(a.get('diagrams', [])) for a in ARTICLES)
if len(docs) != len(ARTICLES) + 7 or len(svg_paths) != expected_diagrams:
    errors.append('Generated page/diagram inventory differs from content inventory')
if docs[(D / 'library.html').resolve()].cards != len(ARTICLES):
    errors.append('Article library inventory differs from content')
terms = {term for a in ARTICLES for term in a['tags']}
if docs[(D / 'glossary.html').resolve()].term_entries != len(terms):
    errors.append('Glossary inventory differs from content')
book = read_json('content/book.json', {'parts': []})
covered = [slug for part in book['parts'] for chapter in part['chapters'] for slug in chapter['slugs']]
if len(covered) != len(set(covered)) or set(covered) != slugs:
    errors.append('Book contents must cover every article exactly once')
for article in ARTICLES:
    if article.get('level') == '深入':
        if len(article['sections']) < 8 or sum(len(s['text']) for s in article['sections']) < 1400:
            errors.append(f'Deep chapter lacks substantive sections: {article["slug"]}')
        if len(article.get('diagrams', [])) < 2 or not article.get('comparison'):
            errors.append(f'Deep chapter lacks supporting diagrams/comparison: {article["slug"]}')
    for detail in article.get('diagrams', []):
        if len(detail['nodes']) != 4 or not detail.get('title') or not detail.get('caption'):
            errors.append(f'Invalid detail diagram: {article["slug"]}')
        if detail.get('diagram_type') not in {'flow', 'comparison', 'branch', 'cycle', 'timeline'}:
            errors.append(f'Unknown detail diagram type: {article["slug"]}')
projects = read_json('content/research/projects.json', [])
resources = read_json('content/research/resources.json', [])
if len(projects) < 30 or len(resources) < 8:
    errors.append('Insufficient researched project/resource coverage')
for collection in (projects, resources):
    identifiers = [item['id'] for item in collection]
    if len(identifiers) != len(set(identifiers)):
        errors.append('Duplicate research item id')
    for item in collection:
        star = item['stars']
        if star['count'] is not None and (not isinstance(star['count'], int) or star['count'] < 0):
            errors.append(f'Invalid star count: {item["id"]}')
        if not star['source'].startswith('https://') or not star.get('as_of') or not star.get('method'):
            errors.append(f'Missing star provenance: {item["id"]}')
        if not item['license'].get('name') or not item['license'].get('source'):
            errors.append(f'Missing license provenance: {item["id"]}')
for item in projects:
    for field in ('role','mechanism','why_learn','when_use','limits','alternatives'):
        if not item.get(field):
            errors.append(f'Project missing {field}: {item["id"]}')

if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(ARTICLES)} articles; {len(docs)} HTML pages; {len(svg_paths)} SVG diagrams; '
      f'{len(terms)} terms; local links, fragments, prerequisites and Markdown checked.')
