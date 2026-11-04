"""Build the bilingual-term, Chinese reading site using the Python standard library."""
import html
import math
import shutil
from pathlib import Path

from catalog import ROOT, load_articles
from diagrams import render as diagram

D = ROOT / 'dist'
A = load_articles()
BY_SLUG = {a['slug']: a for a in A}
CATEGORIES = list(dict.fromkeys(a['category'] for a in A))
TERMS = {}
for article in A:
    for term in article['tags']:
        TERMS.setdefault(term, []).append(article)
N, C, T = len(A), len(CATEGORIES), len(TERMS)
E = html.escape
REPO = 'https://github.com/laihuannran/ai-knowledge'
if D.exists():
    shutil.rmtree(D)
(D / 'articles').mkdir(parents=True)
(D / 'diagrams').mkdir()
shutil.copytree(ROOT / 'assets', D / 'assets')


def page(title, body, sub=False):
    p = '../' if sub else './'
    return f'''<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="面向零基础的 AI 图解知识库。从大模型、RAG、Agent，到推理网关、智能路由、PD 分离与模型评测。">
<meta name="color-scheme" content="light"><title>{E(title)} · AI 慢慢懂</title>
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{p}assets/style.css"><script src="{p}assets/app.js" defer></script>
</head><body><a class="skip" href="#main">跳到正文</a>
<aside class="sidebar"><a class="brand" href="{p}index.html"><span class="brand-symbol">知</span><span>AI 慢慢懂<small>HUANRAN’S FIELD NOTES</small></span></a>
<p class="sidebar-intro">把陌生的技术，<br>变成能理解的知识。</p>
<nav aria-label="主导航"><a href="{p}index.html">知识文章 <span>{N}</span></a><a href="{p}map.html">知识地图 <span>↗</span></a><a href="{p}glossary.html">术语速查 <span>A—Z</span></a><a href="{p}about.html">关于与来源 <span>↗</span></a></nav>
<div class="side-note"><span class="tiny-label">阅读方式</span><p>不赶进度，不写代码。<br>从一个好奇的问题开始。</p></div>
<a class="github" href="{REPO}">GitHub 源码 ↗</a><small class="sidebar-bottom">整理于 2026.11.04<br>中文图解 · 随时翻阅</small></aside>
<div class="shell"><header class="topbar"><span>一份写给普通人的 AI 知识手册</span><a href="{p}map.html">从哪里开始？ ↗</a></header>
<main id="main">{body}</main><footer>AI 慢慢懂 <span>原创讲解与示意图 · 原始资料见各篇文末</span><a href="{p}about.html">编辑说明</a></footer></div></body></html>'''


def search_text(a):
    parts = [a['title'], a['summary'], a['category'], *a['tags'], a['analogy'],
             a['example'], a['pitfall'], a['question'], a['answer'],
             *[s['title'] + ' ' + s['text'] for s in a['sections']]]
    table = a.get('comparison', {})
    parts += table.get('headers', [])
    for row in table.get('rows', []):
        parts.extend(row)
    return ' '.join(parts)


def card(a, i):
    text = search_text(a)
    return f'''<article class="article-card" data-category="{E(a['category'])}" data-search="{E(text)}">
<div class="card-meta"><span>{i+1:02d} / {E(a['category'])} · {E(a.get('level', '入门'))}</span><span>约 {max(3, math.ceil(len(text)/260))} 分钟</span></div>
<h3><a href="articles/{a['slug']}.html">{E(a['title'])}</a></h3><p>{E(a['summary'])}</p>
<div class="card-bottom"><span>{' · '.join(E(t) for t in a['tags'][:3])}</span><a aria-label="阅读：{E(a['title'])}" href="articles/{a['slug']}.html">阅读 ↗</a></div></article>'''


hero = f'''<section class="hero"><div><p class="eyebrow">THE AI FIELD GUIDE / VOL. 02</p><h1>AI 很大，<br>我们<span>慢慢懂。</span></h1>
<p class="hero-copy">从“什么是大模型”到“PD 分离为什么存在”，<br>用图解、类比和真实场景，把知识一点点串起来。</p>
<a class="primary-link" href="articles/ai-map.html">从第一篇开始 <span>→</span></a>
<div class="hero-stats"><span><b>{C:02d}</b> 个专题</span><span><b>{N:02d}</b> 篇图解</span><span><b>00</b> 编程门槛</span></div></div>
<div class="hero-art" aria-label="AI 知识的四层结构"><span class="art-top">把零散名词，放回一张地图</span>
<div class="stack s1"><small>01 / WHAT WE USE</small><b>应用与智能体</b><span>RAG · Agent · MCP</span></div>
<div class="stack s2"><small>02 / HOW WE CONNECT</small><b>接入与治理</b><span>网关 · 路由 · 配额</span></div>
<div class="stack s3"><small>03 / HOW IT RUNS</small><b>模型与推理</b><span>Transformer · KV Cache · PD</span></div>
<div class="stack s4"><small>04 / HOW WE KNOW</small><b>评测与运行</b><span>质量 · 延迟 · 成本</span></div>
<span class="art-bottom">理解关系，比记住名词更重要。</span></div></section>'''
filters = f'<button class="active" data-filter="all" aria-pressed="true">全部文章 <span>{N}</span></button>'
filters += ''.join(f'<button data-filter="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in CATEGORIES)
body = hero + f'''<section class="library" aria-labelledby="library-title"><div class="section-head"><div><p class="eyebrow">READ AT YOUR OWN PACE</p><h2 id="library-title">今天，想弄懂什么？</h2></div>
<label class="search"><span>⌕</span><input id="search" type="search" placeholder="搜一搜：RAG、智能路由、PD…" aria-label="搜索文章全文"></label></div>
<div class="filters" aria-label="按专题筛选">{filters}</div><p class="result-count" aria-live="polite">共 {N} 篇，按理解顺序排列</p>
<div class="article-grid">{''.join(card(a, i) for i, a in enumerate(A))}</div><p id="empty" hidden>没有找到相关内容。试试其他术语，或选择“全部文章”。</p></section>
<section class="reading-note"><span>不知道先读哪篇？</span><p>每个专题先入门、再进阶。文章里的前置知识和关联阅读，会帮你找到下一步。</p><a href="map.html">打开知识地图 →</a></section>'''
(D / 'index.html').write_text(page('首页', body))


def article_links(slugs):
    return ''.join(f'<li><a href="{slug}.html">{E(BY_SLUG[slug]["title"])}</a></li>' for slug in slugs)


def comparison_html(table):
    headers = ''.join(f'<th scope="col">{E(v)}</th>' for v in table['headers'])
    rows = ''.join('<tr>' + ''.join(f'<td>{E(v)}</td>' for v in row) + '</tr>' for row in table['rows'])
    return f'<div class="table-scroll" role="region" aria-label="知识点对比表，可左右滚动" tabindex="0"><table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table></div>'


for i, a in enumerate(A):
    (D / 'diagrams' / f'{a["slug"]}.svg').write_text(diagram(a, i + 1))
    sections = []
    prerequisites = a.get('prerequisites', [])
    if prerequisites:
        sections.append(('先读哪些知识', '<ul>' + article_links(prerequisites) + '</ul>'))
    sections += [
        ('先用一个类比理解', f'<div class="analogy">{E(a["analogy"])}</div><p class="muted">类比只帮助建立直觉，不等同于技术的完整机制。</p>'),
        ('一图看懂', f'<figure><img src="../diagrams/{a["slug"]}.svg" alt="{E("；".join(a["nodes"]))}" width="840" loading="lazy"><figcaption>原创概念示意 · 简化表示，窄屏可左右滑动</figcaption></figure>'),
    ]
    sections.extend((s['title'], f'<p>{E(s["text"])}</p>') for s in a['sections'])
    if a.get('comparison'):
        sections.append(('放在一起对比', comparison_html(a['comparison'])))
    sections += [
        ('放进真实场景', f'<div class="example"><span class="tiny-label">SCENARIO</span><p>{E(a["example"])}</p></div>'),
        ('别踩这个误区', f'<div class="pitfall">{E(a["pitfall"])}</div>'),
        ('想一想', f'<details><summary>{E(a["question"])}</summary><p>{E(a["answer"])}</p></details>'),
    ]
    related = a.get('related')
    if related is None:
        same = [x['slug'] for x in A if x['category'] == a['category'] and x != a]
        related = same[:4]
        if not related:
            related = [A[(i + 1) % N]['slug']]
    related = list(dict.fromkeys(related))
    sections.append(('关联阅读', '<ul>' + article_links(related) + '</ul>'))
    refs = ''.join(f'<li><a href="{E(s["url"])}" rel="noreferrer">{E(s["title"])} ↗</a></li>' for s in a['sources'])
    sections.append(('资料与边界', f'<p>本文为原创知识讲解。类比和图示经过简化；示例数字不代表实测或报价。整理日期：{a["date"]}。文末列出对应技术的原始资料，具体功能与版本支持请以原文为准。</p><ul>{refs}</ul>'))
    toc = ''.join(f'<a href="#section-{j}">{E(title)}</a>' for j, (title, _) in enumerate(sections))
    chunks = ''.join(f'<section id="section-{j}"{(" class=" + chr(34) + "sources" + chr(34)) if title == "资料与边界" else ""}><h2>{E(title)}</h2>{content}</section>' for j, (title, content) in enumerate(sections))
    prev = f'<a href="{A[i-1]["slug"]}.html">← 上一篇<br><b>{E(A[i-1]["title"])}</b></a>' if i else '<a href="../map.html">← 返回知识地图</a>'
    nxt = f'<a href="{A[i+1]["slug"]}.html">下一篇 →<br><b>{E(A[i+1]["title"])}</b></a>' if i+1 < N else '<a href="../index.html">回到文章首页 →</a>'
    content = f'''<div class="breadcrumb"><a href="../index.html">知识文章</a> / {E(a['category'])}</div>
<header class="article-header"><p class="eyebrow">FIELD NOTE {i+1:02d} / {E(a['category'])} / {E(a.get('level', '入门'))}</p><h1>{E(a['title'])}</h1>
<p class="article-lead">{E(a['summary'])}</p><div class="article-meta">整理于 {a['date']} · {E(a['requires'])}</div>
<div class="tag-row">{''.join(f'<span>{E(t)}</span>' for t in a['tags'])}</div></header>
<div class="article-layout"><article class="prose">{chunks}<nav class="prev-next" aria-label="文章翻页">{prev}{nxt}</nav></article>
<aside class="toc"><span class="tiny-label">这篇怎么读</span>{toc}<a class="back-top" href="#main">↑ 回到顶部</a></aside></div>'''
    (D / 'articles' / f'{a["slug"]}.html').write_text(page(a['title'], content, True))

    md = f'# {a["title"]}\n\n> {a["summary"]}\n\n专题：{a["category"]} · 整理于 {a["date"]}\n\n'
    if prerequisites:
        md += '## 前置阅读\n\n' + '\n'.join(f'- [{BY_SLUG[s]["title"]}]({s}.md)' for s in prerequisites) + '\n\n'
    md += f'## 先用一个类比理解\n\n{a["analogy"]}\n\n类比只帮助建立直觉，不等同于完整机制。\n\n## 一图看懂\n\n![{a["summary"]}](../dist/diagrams/{a["slug"]}.svg)\n\n'
    md += '\n\n'.join(f'## {s["title"]}\n\n{s["text"]}' for s in a['sections'])
    if a.get('comparison'):
        table = a['comparison']
        md += '\n\n## 放在一起对比\n\n| ' + ' | '.join(table['headers']) + ' |\n'
        md += '| ' + ' | '.join('---' for _ in table['headers']) + ' |\n'
        md += '\n'.join('| ' + ' | '.join(v.replace('|', '\\|') for v in row) + ' |' for row in table['rows'])
    md += f'\n\n## 真实场景\n\n{a["example"]}\n\n## 常见误区\n\n{a["pitfall"]}\n\n## 想一想\n\n{a["question"]}\n\n<details><summary>查看解释</summary>\n\n{a["answer"]}\n\n</details>\n\n## 关联阅读\n\n'
    md += '\n'.join(f'- [{BY_SLUG[s]["title"]}]({s}.md)' for s in related)
    md += '\n\n## 原始资料\n\n' + '\n'.join(f'- [{s["title"]}]({s["url"]})' for s in a['sources'])
    md += '\n\n原创讲解；图示和类比经过简化，数字示例不代表实测。工具功能以对应版本官方资料为准。\n'
    (ROOT / 'content' / f'{a["slug"]}.md').write_text(md)

map_body = '''<header class="page-heading"><p class="eyebrow">FIND YOUR WAY</p><h1>一张地图，<br>把知识串起来。</h1><p>每个专题先入门、再进阶。无需按计划打卡，带着问题跳读也可以。</p></header><div class="roadmap">'''
for i, category in enumerate(CATEGORIES):
    items = ''.join(f'<li><span class="map-level">{E(a.get("level", "入门"))}</span><a href="articles/{a["slug"]}.html">{E(a["title"])}</a></li>' for a in A if a['category'] == category)
    map_body += f'<section><span class="map-number">{i+1:02d}</span><div><h2>{E(category)}</h2><ul>{items}</ul></div></section>'
routes = [
    ('先听懂常见术语', ['ai-map', 'tokens-context', 'industry-stack']),
    ('理解知识库和智能体', ['prompt', 'rag', 'rag-finetune', 'agent', 'mcp', 'evaluation']),
    ('看懂推理基础设施', ['gateway', 'routing', 'gpu-memory', 'prefill-decode', 'pd-disaggregation', 'latency-cost']),
]
map_body += '</div><section class="reading-note"><span>三条轻量阅读路线</span>'
for title, slugs in routes:
    links = ' → '.join(f'<a href="articles/{s}.html">{E(BY_SLUG[s]["title"].split("：")[0])}</a>' for s in slugs)
    map_body += f'<p><b>{title}</b><br>{links}</p>'
map_body += '</section>'
(D / 'map.html').write_text(page('知识地图', map_body))

gloss = f'''<header class="page-heading"><p class="eyebrow">A SMALL DICTIONARY</p><h1>陌生名词，<br>随时查一查。</h1><p>{T} 个术语入口。点开文章，查看定义、关系和例子。</p></header><label class="search glossary-search"><span>⌕</span><input id="term-search" type="search" placeholder="搜索术语" aria-label="搜索术语"></label><div class="glossary">'''
for term, items in sorted(TERMS.items(), key=lambda pair: pair[0].casefold()):
    links = ''.join(f'<a href="articles/{a["slug"]}.html">{E(a["title"])} ↗</a>' for a in items)
    gloss += f'<section data-term="{E(term.lower())}"><h2>{E(term)}</h2>{links}</section>'
gloss += '</div><p id="term-empty" aria-live="polite" hidden>未找到对应术语。</p>'
(D / 'glossary.html').write_text(page('术语速查', gloss))

about = f'''<header class="page-heading"><p class="eyebrow">ABOUT THIS NOTEBOOK</p><h1>写给刚开始<br>理解 AI 的你。</h1><p>不用先会编程，也不必追着每个新名词跑。</p></header><article class="prose about">
<h2>这是什么？</h2><p>这是 laihuannran 的 AI 图解知识库，目前按 {C} 个专题整理 {N} 篇文章。每篇配有概念图，部分内容增加对比表。目标是理解术语、机制和选择的依据，不要求编程。你可以从入门篇开始，再沿前置阅读和关联链接深入。</p>
<h2>资料怎么来？</h2><p>优先参考官方文档、官方项目与原始技术说明，使用原创中文解释和 SVG 示意图。各篇文末链接用于追溯技术概念，不是照搬或翻译整篇原文。整理日期在文章中标注；产品状态和版本支持仍以原文为准。网络可达性记录与人工概念核验是不同检查。</p>
<h2>怎么看图和例子？</h2><p>图示突出概念关系，省略部分实现细节。类比只用于建立直觉。假设数字、费用算式与业务场景用于教学，不代表实测性能、厂商报价或采购建议。</p>
<h2>覆盖到哪里？</h2><p>本站覆盖从基础到平台工程的主要概念与常见技术栈，不声称包含全部 AI 知识。学习型资料会继续补充和修正；高级算法证明、完整训练配方及厂商具体部署参数不属于当前阅读目标。</p>
<h2>如何维护？</h2><p>文字、图示和构建源码存放在 GitHub，内容更新通过提交发布。当前没有设置定时采集或自动写文章的任务。</p>
<h2>版权与使用</h2><p>本站原创文字和示意图采用 CC BY 4.0；第三方资料归原作者，遵循其各自许可。构建代码采用 MIT 许可。</p><p><a href="https://creativecommons.org/licenses/by/4.0/deed.zh-hans">查看 CC BY 4.0</a> · <a href="{REPO}">查看 GitHub 仓库 ↗</a></p></article>'''
(D / 'about.html').write_text(page('关于与来源', about))
(D / '.nojekyll').touch()
print(f'Built {N} articles, {C} categories, {T} terms, {len(list(D.rglob("*.html")))} HTML pages')
