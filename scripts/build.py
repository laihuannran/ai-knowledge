"""Build the reading site using only Python's standard library."""
from pathlib import Path
import json,html,shutil,re,math
R=Path(__file__).resolve().parents[1]; D=R/'dist'
if D.exists(): shutil.rmtree(D)
(D/'articles').mkdir(parents=True); (D/'diagrams').mkdir(); shutil.copytree(R/'assets',D/'assets')
A=json.loads((R/'content/articles.json').read_text()); cats=list(dict.fromkeys(a['category'] for a in A)); E=html.escape
REPO='https://github.com/laihuannran/ai-knowledge'
def page(title,body,sub=False):
 p='../' if sub else './'
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="面向零基础的 AI 图解知识库。从大模型、RAG、Agent，到推理网关、智能路由、PD 分离与模型评测。"><meta name="color-scheme" content="light"><title>{E(title)} · AI 慢慢懂</title><link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{p}assets/style.css"><script src="{p}assets/app.js" defer></script></head><body><a class="skip" href="#main">跳到正文</a><aside class="sidebar"><a class="brand" href="{p}index.html"><span class="brand-symbol">知</span><span>AI 慢慢懂<small>HUANRAN’S FIELD NOTES</small></span></a><p class="sidebar-intro">把陌生的技术，<br>变成能理解的知识。</p><nav aria-label="主导航"><a href="{p}index.html">知识文章 <span>20</span></a><a href="{p}map.html">知识地图 <span>↗</span></a><a href="{p}glossary.html">术语速查 <span>A—Z</span></a><a href="{p}about.html">关于与来源 <span>↗</span></a></nav><div class="side-note"><span class="tiny-label">阅读方式</span><p>不赶进度，不写代码。<br>从一个好奇的问题开始。</p></div><a class="github" href="{REPO}">GitHub 源码 ↗</a><small class="sidebar-bottom">整理于 2026.11.04<br>中文图解 · 随时翻阅</small></aside><div class="shell"><header class="topbar"><span>一份写给普通人的 AI 知识手册</span><a href="{p}map.html">从哪里开始？ ↗</a></header><main id="main">{body}</main><footer>AI 慢慢懂 <span>原创讲解与示意图 · 原始资料见各篇文末</span><a href="{p}about.html">编辑说明</a></footer></div></body></html>'''
def wrap(text,n=13):
 return [text[i:i+n] for i in range(0,len(text),n)]
def svg(a):
 title=a['title']; nodes=a['nodes']; parallel=a['slug'] in ['rag-finetune','gpu-memory','model-choices','industry-stack','serving-stack']; nested=a['slug']=='ai-map'
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 340" role="img" aria-labelledby="title desc"><title id="title">{E(title)}</title><desc id="desc">{E("；".join(nodes))}</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10" fill="none" stroke="#64746c" stroke-width="1.5"/></marker></defs><rect width="840" height="340" rx="16" fill="#f0f3ed"/><g font-family="PingFang SC,Microsoft YaHei,sans-serif"><text x="28" y="35" fill="#52675c" font-size="12" letter-spacing="2">FIELD NOTE / {A.index(a)+1:02d}</text>']
 if nested:
  for i,node in enumerate(nodes):
   x=35+i*46; y=56+i*51; w=770-i*92; h=265-i*51
   parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{["#d9e5da","#c2d8c8","#a4c4b0","#1f5b49"][i]}"/><text x="{x+18}" y="{y+29}" font-size="16" fill="{"#fff" if i==3 else "#173d31"}">{E(node)}</text>')
 else:
  for i,node in enumerate(nodes):
   x=28+i*204; y=95
   parts.append(f'<rect x="{x}" y="{y}" width="174" height="142" rx="10" fill="{"#1f5b49" if i==3 else "#fff"}" stroke="#cbd9cf"/><text x="{x+15}" y="{y+29}" fill="{"#bdd9cc" if i==3 else "#81978b"}" font-size="12">0{i+1}</text>')
   for j,line in enumerate(wrap(node,10)):
    parts.append(f'<text x="{x+15}" y="{y+62+j*24}" fill="{"#fff" if i==3 else "#173d31"}" font-size="16">{E(line)}</text>')
   if i<3 and not parallel: parts.append(f'<path d="M{x+179} 166h20" stroke="#64746c" fill="none" marker-end="url(#arrow)"/>')
  caption='四个观察维度 · 非顺序流程' if parallel else '从左向右阅读 · 简化流程，实际实现可能不同'
  parts.append(f'<text x="28" y="294" fill="#687a6e" font-size="13">{caption}</text>')
 parts.append('</g></svg>'); return ''.join(parts)

def card(a,i):
 search=' '.join([a['title'],a['summary'],a['category'],*a['tags'],a['analogy'],a['example'],a['pitfall'],*[s['text'] for s in a['sections']]])
 return f'''<article class="article-card" data-category="{E(a['category'])}" data-search="{E(search)}"><div class="card-meta"><span>{i+1:02d} / {E(a['category'])}</span><span>约 {max(3,math.ceil(len(search)/260))} 分钟</span></div><h3><a href="articles/{a['slug']}.html">{E(a['title'])}</a></h3><p>{E(a['summary'])}</p><div class="card-bottom"><span>{' · '.join(E(t) for t in a['tags'][:3])}</span><a aria-label="阅读：{E(a['title'])}" href="articles/{a['slug']}.html">阅读 ↗</a></div></article>'''
hero='''<section class="hero"><div><p class="eyebrow">THE AI FIELD GUIDE / VOL. 01</p><h1>AI 很大，<br>我们<span>慢慢懂。</span></h1><p class="hero-copy">从“什么是大模型”到“PD 分离为什么存在”，<br>用图解、类比和真实场景，把知识一点点串起来。</p><a class="primary-link" href="articles/ai-map.html">从第一篇开始 <span>→</span></a><div class="hero-stats"><span><b>08</b> 个专题</span><span><b>20</b> 篇图解</span><span><b>00</b> 编程门槛</span></div></div><div class="hero-art" aria-label="AI 知识的四层结构"><span class="art-top">把零散名词，放回一张地图</span><div class="stack s1"><small>01 / WHAT WE USE</small><b>应用与智能体</b><span>RAG · Agent · MCP</span></div><div class="stack s2"><small>02 / HOW WE CONNECT</small><b>接入与治理</b><span>网关 · 路由 · 配额</span></div><div class="stack s3"><small>03 / HOW IT RUNS</small><b>模型与推理</b><span>Transformer · KV Cache · PD</span></div><div class="stack s4"><small>04 / HOW WE KNOW</small><b>评测与运行</b><span>质量 · 延迟 · 成本</span></div><span class="art-bottom">理解关系，比记住名词更重要。</span></div></section>'''
filters='<button class="active" data-filter="all" aria-pressed="true">全部文章 <span>20</span></button>'+''.join(f'<button data-filter="{E(c)}" aria-pressed="false">{E(c)}</button>' for c in cats)
body=hero+f'''<section class="library" aria-labelledby="library-title"><div class="section-head"><div><p class="eyebrow">READ AT YOUR OWN PACE</p><h2 id="library-title">今天，想弄懂什么？</h2></div><label class="search"><span>⌕</span><input id="search" type="search" placeholder="搜一搜：RAG、智能路由、PD…" aria-label="搜索文章全文"></label></div><div class="filters" aria-label="按专题筛选">{filters}</div><p class="result-count" aria-live="polite">共 20 篇，按理解顺序排列</p><div class="article-grid">{''.join(card(a,i) for i,a in enumerate(A))}</div><p id="empty" hidden>没有找到相关内容。试试其他术语，或选择“全部文章”。</p></section><section class="reading-note"><span>不知道先读哪篇？</span><p>先理解基础，再看应用；遇到陌生词，可以随时回到知识地图。</p><a href="map.html">打开知识地图 →</a></section>'''
(D/'index.html').write_text(page('首页',body))
for i,a in enumerate(A):
 (D/'diagrams'/f'{a["slug"]}.svg').write_text(svg(a))
 headings=['先用一个类比理解','一图看懂']+[s['title'] for s in a['sections']]+['放进真实场景','别踩这个误区','想一想','关联阅读','资料与边界']
 toc=''.join(f'<a href="#section-{j}">{E(t)}</a>' for j,t in enumerate(headings))
 chunks=[f'<section id="section-0"><h2>先用一个类比理解</h2><div class="analogy">{E(a["analogy"])}</div><p class="muted">类比只帮助建立直觉，不等同于技术的完整机制。</p></section>',f'<section id="section-1"><h2>一图看懂</h2><figure><img src="../diagrams/{a["slug"]}.svg" alt="{E("；".join(a["nodes"]))}" width="840" height="340"><figcaption>原创概念示意 · {E(a["category"])} · 简化表示，窄屏可左右滑动</figcaption></figure></section>']
 j=2
 for s in a['sections']:
  chunks.append(f'<section id="section-{j}"><h2>{E(s["title"])}</h2><p>{E(s["text"])}</p></section>'); j+=1
 chunks.append(f'<section id="section-{j}"><h2>放进真实场景</h2><div class="example"><span class="tiny-label">SCENARIO</span><p>{E(a["example"])}</p></div></section>'); j+=1
 chunks.append(f'<section id="section-{j}"><h2>别踩这个误区</h2><div class="pitfall">{E(a["pitfall"])}</div></section>'); j+=1
 chunks.append(f'<section id="section-{j}"><h2>想一想</h2><details><summary>{E(a["question"])}</summary><p>{E(a["answer"])}</p></details></section>'); j+=1
 related=[x for x in A if x['category']==a['category'] and x!=a]
 if len(related)<2: related += [A[(i+1)%len(A)]]
 seen=set(); rel=[]
 for x in related:
  if x['slug'] not in seen: rel.append(f'<li><a href="{x["slug"]}.html">{E(x["title"])}</a></li>');seen.add(x['slug'])
 chunks.append(f'<section id="section-{j}"><h2>关联阅读</h2><ul>{"".join(rel)}</ul></section>'); j+=1
 refs=''.join(f'<li><a href="{E(s["url"])}" rel="noreferrer">{E(s["title"])} ↗</a></li>' for s in a['sources'])
 chunks.append(f'<section class="sources" id="section-{j}"><h2>资料与边界</h2><p>以下是对应技术的官方文档或项目入口。本文为原创入门讲解，图示与场景经过简化；示例数字不代表实测或报价。整理日期：{a["date"]}。工具功能与版本支持会变化，请以原始资料为准。</p><ul>{refs}</ul></section>')
 prev=f'<a href="{A[i-1]["slug"]}.html">← 上一篇<br><b>{E(A[i-1]["title"])}</b></a>' if i else '<a href="../map.html">← 返回知识地图</a>'
 nxt=f'<a href="{A[i+1]["slug"]}.html">下一篇 →<br><b>{E(A[i+1]["title"])}</b></a>' if i+1<len(A) else '<a href="../index.html">回到文章首页 →</a>'
 content=f'''<div class="breadcrumb"><a href="../index.html">知识文章</a> / {E(a['category'])}</div><header class="article-header"><p class="eyebrow">FIELD NOTE {i+1:02d} / {E(a['category'])}</p><h1>{E(a['title'])}</h1><p class="article-lead">{E(a['summary'])}</p><div class="article-meta">整理于 {a['date']} · {E(a['requires'])}</div><div class="tag-row">{''.join(f'<span>{E(t)}</span>' for t in a['tags'])}</div></header><div class="article-layout"><article class="prose">{''.join(chunks)}<nav class="prev-next" aria-label="文章翻页">{prev}{nxt}</nav></article><aside class="toc"><span class="tiny-label">这篇怎么读</span>{toc}<a class="back-top" href="#main">↑ 回到顶部</a></aside></div>'''
 (D/'articles'/f'{a["slug"]}.html').write_text(page(a['title'],content,True))
 # Markdown is also readable directly in the GitHub repository.
 md=f'# {a["title"]}\n\n> {a["summary"]}\n\n专题：{a["category"]} · 整理于 {a["date"]}\n\n## 先用一个类比理解\n\n{a["analogy"]}\n\n## 一图看懂\n\n![{a["summary"]}](../dist/diagrams/{a["slug"]}.svg)\n\n'
 md+='\n\n'.join(f'## {s["title"]}\n\n{s["text"]}' for s in a['sections'])
 md+=f'\n\n## 真实场景\n\n{a["example"]}\n\n## 常见误区\n\n{a["pitfall"]}\n\n## 想一想\n\n{a["question"]}\n\n<details><summary>查看解释</summary>\n\n{a["answer"]}\n\n</details>\n\n## 原始资料\n\n'+ '\n'.join(f'- [{s["title"]}]({s["url"]})' for s in a['sources'])+'\n\n原创入门讲解；类比和示意图经过简化。工具功能以对应版本官方文档为准。\n'
 (R/'content'/f'{a["slug"]}.md').write_text(md)
map_body='<header class="page-heading"><p class="eyebrow">FIND YOUR WAY</p><h1>一张地图，<br>把知识串起来。</h1><p>按顺序读可以，带着问题跳读也可以。每个专题都是一个入口。</p></header><div class="roadmap">'
for i,c in enumerate(cats):
 items=''.join(f'<li><a href="articles/{a["slug"]}.html">{E(a["title"])}</a></li>' for a in A if a['category']==c)
 map_body+=f'<section><span class="map-number">{i+1:02d}</span><div><h2>{E(c)}</h2><ul>{items}</ul></div></section>'
map_body+='</div><div class="reading-note"><span>三条轻量阅读路线</span><p>只想听懂：AI 地图 → Token → 行业技术栈<br>关心应用：提示词 → RAG → Agent → MCP → 评测<br>关心平台：网关 → 路由 → GPU → KV Cache → PD 分离 → 性能指标</p></div>'
(D/'map.html').write_text(page('知识地图',map_body))
terms={}
for a in A:
 for t in a['tags']: terms.setdefault(t,[]).append(a)
gloss='<header class="page-heading"><p class="eyebrow">A SMALL DICTIONARY</p><h1>陌生名词，<br>随时查一查。</h1><p>点开术语对应的文章，看定义、关系与具体例子。</p></header><label class="search glossary-search"><span>⌕</span><input id="term-search" type="search" placeholder="搜索术语" aria-label="搜索术语"></label><div class="glossary">'
for t,items in sorted(terms.items(),key=lambda x:x[0].casefold()):
 links=''.join(f'<a href="articles/{a["slug"]}.html">{E(a["title"])} ↗</a>' for a in items)
 gloss+=f'<section data-term="{E(t.lower())}"><h2>{E(t)}</h2>{links}</section>'
gloss+='</div><p id="term-empty" hidden>未找到对应术语。</p>'
(D/'glossary.html').write_text(page('术语速查',gloss))
about='''<header class="page-heading"><p class="eyebrow">ABOUT THIS NOTEBOOK</p><h1>写给刚开始<br>理解 AI 的你。</h1><p>不用先会编程，也不必追着每个新名词跑。</p></header><article class="prose about"><h2>这是什么？</h2><p>这是 laihuannran 的 AI 图解知识库，按八个专题整理 20 篇入门文章。目标是理解术语和技术之间的关系，而不是提供算法训练课或部署操作手册。你可以从第一篇开始，也可以从工作中听到的名词进入。</p><h2>资料怎么来？</h2><p>优先参考官方文档、官方项目与原始技术说明，使用原创中文解释和 SVG 示意图，不转载同事博客文章。各篇文末链接用于追溯技术定义。文章按 2026-11-04 的整理批次记录，链接可达性检查另见仓库记录；不保证所有上游页面和产品状态永久不变。</p><h2>怎么看图和例子？</h2><p>图示突出概念关系，省略部分实现细节。生活类比只用于建立直觉。假设数字、费用算式与业务场景用于教学，不是实测结果、厂商报价或采购承诺。</p><h2>如何维护？</h2><p>正文与结构化数据存放在 GitHub 仓库，网站由静态文件构成。后续可以继续扩展专题、纠错和添加资料；当前没有设置定时采集或自动发布任务。</p><h2>版权与使用</h2><p>本站原创文字和示意图采用 CC BY 4.0；引用链接所指向的资料归原作者所有，遵循其各自许可。网站构建代码采用 MIT 许可。</p><p><a href="https://creativecommons.org/licenses/by/4.0/deed.zh-hans">查看 CC BY 4.0</a> · <a href="https://github.com/laihuannran/ai-knowledge">查看 GitHub 仓库 ↗</a></p></article>'''
(D/'about.html').write_text(page('关于与来源',about)); (D/'.nojekyll').touch()
print(f'Built {len(A)} articles, {len(terms)} terms, {len(list(D.rglob("*.html")))} HTML pages')
