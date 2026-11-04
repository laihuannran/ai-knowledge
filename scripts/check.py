"""Check site integrity, local links, fragments, SVG validity and editorial fields."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];D=R/'dist';errors=[]
class Doc(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for k in ['href','src']:
   if a.get(k):self.links.append(a[k])
  if tag=='img' and not a.get('alt'):errors.append('Image without alt')
docs={}
for p in D.rglob('*.html'):
 q=Doc();q.feed(p.read_text());docs[p.resolve()]=q
for p,q in docs.items():
 for link in q.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  if not target.is_relative_to(D.resolve()):errors.append(f'Escapes site: {p}: {link}')
  elif not target.exists():errors.append(f'Broken link: {p}: {link}')
  elif u.fragment and target in docs and unquote(u.fragment) not in docs[target].ids:errors.append(f'Broken fragment: {p}: {link}')
for p in (D/'diagrams').glob('*.svg'):ET.parse(p)
a=json.loads((R/'content/articles.json').read_text());slugs=set()
for item in a:
 if item['slug'] in slugs:errors.append('Duplicate slug')
 slugs.add(item['slug'])
 for k in ['summary','analogy','nodes','sections','example','pitfall','question','answer','sources']:
  if not item.get(k):errors.append(f'Missing {k}: {item["slug"]}')
 if len(item['nodes'])!=4:errors.append('Expected four diagram nodes')
 for s in item['sources']:
  if not s['url'].startswith('https://'):errors.append('Expected HTTPS source')
assert len(a)==20 and len(docs)==24
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(a)} articles; {len(docs)} HTML pages; 20 SVG diagrams; all local paths and fragments valid.')
