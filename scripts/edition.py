"""Book navigation, researched stack atlas and reference shelf, rendered as static HTML."""
import html
import json
import math
from collections import Counter
from catalog import ROOT

E = html.escape
PROJECT_CATEGORIES = {
    'appframeworks': '应用与检索框架', 'agents': 'Agent 框架',
    'lowcode': '低代码与自动化', 'codingassistants': '编程 Agent',
    'client': '应用客户端', 'runtime': '本地模型运行时', 'serving': '推理引擎与集群',
    'gateway': '模型网关', 'data': '数据、检索与缓存', 'eval': '评测与可观测性',
    'frontend': '前端与交互', 'protocol': '工具与协作协议', 'messaging': '消息与事件',
}
PROJECT_CHAPTERS = {
    'LangChain': 'stack-langchain', 'LangGraph': 'stack-langgraph-state',
    'LlamaIndex': 'stack-rag-frameworks', 'Haystack': 'stack-rag-frameworks',
    'Spring AI': 'stack-java-ai', 'LangChain4j': 'stack-java-ai',
    'CrewAI': 'stack-agent-frameworks', 'AutoGen': 'stack-agent-frameworks',
    'OpenAI Agents SDK': 'stack-agent-frameworks', 'Google ADK': 'stack-agent-frameworks',
    'smolagents': 'stack-agent-frameworks', 'Microsoft Agent Framework': 'stack-agent-frameworks',
    'Dify': 'stack-lowcode', 'n8n': 'stack-lowcode', 'Flowise': 'stack-lowcode',
    'Codex CLI': 'stack-codex', 'Claude Code': 'stack-claude',
    'Open WebUI': 'stack-local-clients', 'LibreChat': 'stack-local-clients',
    'Ollama': 'stack-local-clients', 'llama.cpp': 'stack-local-clients',
    'vLLM': 'deep-pd-trace', 'SGLang': 'deep-pd-trace', 'llm-d': 'deep-pd-trace',
    'LiteLLM': 'deep-gateway-lifecycle', 'Envoy AI Gateway': 'deep-gateway-lifecycle',
    'pgvector': 'vector-index', 'Milvus': 'vector-index', 'Qdrant': 'vector-index',
    'Elasticsearch': 'deep-rag-retrieval', 'Redis': 'deep-stack-architecture',
    'Apache Kafka': 'deep-stack-architecture', 'Kafka': 'deep-stack-architecture',
    'Langfuse': 'deep-eval-production', 'MLflow': 'deep-eval-production',
    'Ragas': 'deep-eval-design', 'DeepEval': 'deep-eval-design',
    'lm-evaluation-harness': 'deep-eval-design', 'React': 'stack-java-ai',
    'Vercel AI SDK': 'stack-java-ai', 'MCP Python SDK': 'stack-protocols',
    'A2A': 'stack-protocols',
    'Microsoft GraphRAG': 'graphrag-indexing', 'LightRAG': 'graphrag-querying',
    'Graphiti': 'memory-lifecycle', 'Mem0': 'memory-lifecycle', 'Letta': 'memory-lifecycle',
    'Anthropic Skills 示例': 'skills-loading', 'Agent Skills 规范': 'skills-loading',
    'Neo4j': 'graphrag-indexing',
}


def read_json(path, fallback):
    file = ROOT / path
    return json.loads(file.read_text()) if file.exists() else fallback


def paragraphs(text):
    return ''.join(f'<p>{E(p)}</p>' for p in text.split('\n\n') if p.strip())


def stars_html(stars):
    count = stars.get('count')
    number = f'{count:,}' if count is not None else '未获取'
    return f'<a class="star-count" href="{E(stars["source"])}" title="{E(stars.get("method", ""))}">☆ {number}</a>'


class BookEdition:
    def __init__(self, articles):
        self.articles = articles
        self.by_slug = {a['slug']: a for a in articles}
        self.book = read_json('content/book.json', {'parts': []})
        self.parts = self.book['parts']
        self.learning_review = read_json('content/learning_review.json', {'themes': [], 'questions': [], 'sources': []})
        self.series_count = len({slug for t in self.learning_review['themes'] for slug in t['lessons']})
        self.projects = read_json('content/research/projects.json', [])
        self.resources = read_json('content/research/resources.json', [])
        self.membership = {}
        for pi, part in enumerate(self.parts):
            for ci, chapter in enumerate(part['chapters']):
                for ai, slug in enumerate(chapter['slugs']):
                    self.membership[slug] = (pi, ci, ai, part, chapter)
        self.deep_count = sum(a.get('level') == '深入' for a in articles)

    def sidebar(self, prefix):
        links = ''.join(f'<a href="{prefix}map.html#{E(p["id"])}"><span>{i+1:02d}</span>{E(p["title"])}</a>' for i,p in enumerate(self.parts))
        return f'<details class="sidebar-book" open><summary>全书目录 <span>{len(self.parts)} 篇</span></summary><div>{links}</div></details>'

    def article_context(self, slug):
        if slug not in self.membership:
            return ''
        pi, ci, ai, part, chapter = self.membership[slug]
        siblings = chapter['slugs']
        links = ''.join(f'<a class="{"current" if s == slug else ""}" href="{s}.html"'+ (' aria-current="page"' if s == slug else '') + f'><span>{j+1:02d}</span>{E(self.by_slug[s]["title"])}</a>' for j,s in enumerate(siblings))
        return f'''<section class="chapter-context"><div><span class="eyebrow">第 {pi+1:02d} 篇 / 第 {ci+1:02d} 章</span><a href="../map.html#{E(chapter['id'])}">{E(part['title'])} · {E(chapter['title'])} ↗</a></div><details><summary>本章阅读顺序 · {len(siblings)} 节</summary><nav aria-label="本章目录">{links}</nav></details></section>'''

    def article_breadcrumb(self, slug):
        if slug not in self.membership:
            return '<a href="../map.html">全书目录</a>'
        _, _, _, part, chapter = self.membership[slug]
        return f'<a href="../map.html">全书目录</a> / <a href="../map.html#{E(part["id"])}">{E(part["title"])}</a> / {E(chapter["title"])}'

    def chapter_list(self, chapter, compact=False):
        items = []
        for i, slug in enumerate(chapter['slugs']):
            a = self.by_slug[slug]
            level = a.get('level', '入门')
            tag = '机制与案例' if level == '深入' else '概念入门'
            content_len = sum(len(s['text']) for s in a['sections'])
            mins = max(3, math.ceil(content_len / 240))
            summary = '' if compact else f'<p>{E(a["summary"])}</p>'
            items.append(f'''<li data-book-search="{E(a['title']+' '+a['summary']+' '+' '.join(a['tags']))}"><span class="toc-index">{i+1:02d}</span><div><a href="articles/{slug}.html">{E(a['title'])}</a>{summary}</div><span class="depth-badge {'deep' if level=='深入' else ''}">{tag}<small>{mins} 分钟</small></span></li>''')
        return '<ol class="chapter-reading">' + ''.join(items) + '</ol>'

    def home(self):
        chapters = sum(len(p['chapters']) for p in self.parts)
        cover = '''<div class="book-display" aria-label="AI慢慢懂图解教程封面"><div class="book-cover"><div class="cover-kicker">A FIELD GUIDE TO ARTIFICIAL INTELLIGENCE</div><h2>AI<br>慢慢懂</h2><div class="cover-line"></div><p>从概念，到系统。<br>从模型，到技术栈。</p><span class="cover-mark">图解教程 · 书籍版</span><small>HUANRAN’S LEARNING LIBRARY / 2026</small></div><div class="book-caption">一本可以按顺序读，也可以带着问题翻的书。</div></div>'''
        hero = f'''<section class="book-hero"><div><p class="eyebrow">THE AI LEARNING LIBRARY / BOOK EDITION</p><h1>把 AI，<br>学成<span>一套知识。</span></h1><p class="book-lead">先看懂概念，再走进机制、案例与主流技术栈。<br>无需先会编程，沿着篇章，一层一层读懂。</p><div class="hero-actions"><a class="primary-link" href="map.html">打开全书目录 <span>→</span></a><a class="quiet-link" href="articles/ai-map.html">从第一节开始 ↗</a></div><div class="book-stats"><span><b>{len(self.parts):02d}</b>篇</span><span><b>{chapters}</b>章</span><span><b>{self.deep_count}</b>篇深入讲解</span></div></div>{cover}</section>'''
        routes = '''<section class="entry-routes"><a href="map.html#foundations"><small>01 / BUILD A MENTAL MODEL</small><h3>先听懂 AI 在说什么</h3><p>概念、模型、训练与应用的关系。</p><span>从基础篇进入 →</span></a><a href="stack.html"><small>02 / KNOW THE TOOLBOX</small><h3>认识优秀技术栈</h3><p>LangChain、LangGraph、Agent 与工具链。</p><span>打开技术栈图谱 →</span></a><a href="map.html#inference"><small>03 / UNDERSTAND THE SYSTEM</small><h3>看懂推理与平台</h3><p>网关、路由、KV Cache、PD 与评测。</p><span>从系统机制进入 →</span></a></section>'''
        toc = '<section class="book-overview"><div class="section-head"><div><p class="eyebrow">CONTENTS / FROM THE FIRST PRINCIPLE TO THE STACK</p><h2>这本书，怎样展开？</h2></div><a class="quiet-link" href="map.html">展开完整目录 →</a></div><div class="part-grid">'
        for i,p in enumerate(self.parts):
            count = sum(len(c['slugs']) for c in p['chapters'])
            chapter_names = ' / '.join(c['title'] for c in p['chapters'])
            toc += f'''<a class="part-card" href="map.html#{E(p['id'])}"><span class="part-number">{i+1:02d}</span><div><small>{E(p['subtitle'])}</small><h3>{E(p['title'])}</h3><p>{E(p['description'])}</p><span class="part-meta">{len(p['chapters'])} 章 · {count} 节 <b>↗</b></span><span class="visually-hidden">{E(chapter_names)}</span></div></a>'''
        toc += '</div></section>'
        stack = f'''<section class="stack-teaser"><p class="eyebrow">A MAP OF THE AI ECOSYSTEM</p><h2>不只认识名词，<br>还要知道工具放在哪里。</h2><p>研究 {len(self.projects)} 个项目，按框架、Agent、数据、网关、推理与评测分类。<br>每项都解释职责、机制、适用场景、限制和许可；GitHub 关注度附采集日期。</p><div class="stack-name-row"><span>LangChain</span><span>LangGraph</span><span>Spring AI</span><span>Codex</span><span>vLLM</span><span>Redis</span></div><a class="primary-link" href="stack.html">查看技术栈与比较 <span>→</span></a></section>'''
        note = f'''<section class="reading-note"><span>这是一份怎样的教程？</span><p>{len(self.articles)} 节内容区分概念入门与机制案例。长章节沿着同一条任务链解释细节，配原创图表和原始资料。已有短文作为查阅入口，核心专题继续向深入系列展开。</p><a href="resources.html">查看参考书架与资料来源 →</a></section>'''
        guide = f'<section class="learning-callout"><div><small>NEW SERIES / 把陌生名词连成机制</small><h2>MCP、Skills、GraphRAG，接下来读什么？</h2><p>从概念入口进入{self.series_count}篇独立长章节，再用企业执行问题检验理解。</p></div><a href="guide.html">打开 Agent 进阶路线 →</a></section>'
        return hero + guide + routes + toc + stack + note

    def contents(self):
        out = f'''<header class="page-heading"><p class="eyebrow">TABLE OF CONTENTS / READ LIKE A BOOK</p><h1>从第一篇，<br>读到一套完整架构。</h1><p>{len(self.parts)} 篇 · {sum(len(p['chapters']) for p in self.parts)} 章 · {len(self.articles)} 节。概念入门建立直觉，机制与案例帮助深入理解。</p></header><div class="contents-tools"><label class="search"><span>⌕</span><input id="book-search" type="search" placeholder="在目录中找 LangGraph、RAG、PD…" aria-label="搜索全书目录"></label><button id="expand-toc" type="button">展开全部篇章</button><button id="collapse-toc" type="button">收起全部篇章</button></div><p id="book-results" class="result-count" aria-live="polite">所有章节按理解顺序排列</p><div class="book-contents">'''
        for i,p in enumerate(self.parts):
            chapters = ''
            for j,c in enumerate(p['chapters']):
                chapters += f'''<section id="{E(c['id'])}" class="book-chapter"><div class="chapter-heading"><span>第 {j+1:02d} 章</span><h3>{E(c['title'])}</h3></div><p class="chapter-summary">{E(c['summary'])}</p>{self.chapter_list(c)}</section>'''
            out += f'''<details class="book-part" id="{E(p['id'])}" open><summary><span class="part-number">{i+1:02d}</span><div><small>{E(p['subtitle'])}</small><h2>{E(p['title'])}</h2><p>{E(p['description'])}</p></div><span class="part-toggle" aria-hidden="true">＋</span></summary>{chapters}</details>'''
        out += '</div><p id="book-empty" hidden>没有找到对应章节。可尝试术语别名，或使用文章全文搜索。</p><section class="reading-note"><span>想按问题查阅？</span><p>目录搜索用于定位章节；文章检索会同时搜索正文、术语与比较表。</p><a href="library.html">打开全文检索 →</a></section>'
        return out

    def stack(self):
        categories = list(dict.fromkeys(p['category'] for p in self.projects))
        intro = f'''<header class="page-heading"><p class="eyebrow">THE AI STACK ATLAS / DATED GITHUB SNAPSHOTS</p><h1>优秀工具很多，<br>先看它们各管哪一层。</h1><p>{len(self.projects)} 个项目的职责、机制与取舍。GitHub Star 是关注度快照，逐项标注采集日期，不代表本教程的品质排名。</p></header><section class="architecture-strip" aria-label="技术栈分层"><a href="#project-list" data-role-shortcut="frontend,client">交互与客户端</a><span>→</span><a href="#project-list" data-role-shortcut="appframeworks,agents,lowcode">应用与 Agent</a><span>→</span><a href="#project-list" data-role-shortcut="data">数据与检索</a><span>→</span><a href="#project-list" data-role-shortcut="gateway,serving">网关与推理</a><span>↔</span><a href="#project-list" data-role-shortcut="eval">评测与运行</a></section><div class="stack-guide"><p>先用技术栈专章理解架构，再查项目细节：<a href="articles/stack-langchain.html">LangChain</a> · <a href="articles/stack-langgraph-state.html">LangGraph</a> · <a href="articles/stack-agent-frameworks.html">Agent 框架比较</a> · <a href="articles/stack-codex.html">Codex</a> · <a href="articles/stack-claude.html">Claude</a> · <a href="articles/deep-stack-architecture.html">完整技术栈案例</a></p></div><div class="section-head" id="project-list"><h2>按职责找工具</h2><label class="search"><span>⌕</span><input id="project-search" type="search" placeholder="查找项目、机制、适用场景…" aria-label="搜索技术项目"></label></div><div class="project-filters filters"><button class="active" data-project-filter="all" aria-pressed="true">全部项目</button>'''
        intro += ''.join(f'<button data-project-filter="{E(c)}" aria-pressed="false">{E(PROJECT_CATEGORIES.get(c,c))}</button>' for c in categories)
        intro += f'</div><p class="result-count" id="project-results" aria-live="polite">共 {len(self.projects)} 个项目，按技术职责组织</p><div class="project-grid">'
        for p in self.projects:
            name = p['name'].split('（')[0]
            chapter = PROJECT_CHAPTERS.get(name)
            chapter_link = f'<a class="project-chapter" href="articles/{chapter}.html">进入相关章节 →</a>' if chapter in self.by_slug else ''
            archived = p.get('status', {}).get('archived') is True or '已归档' in p['name']
            badge = '<span class="archive-badge">已归档 · 历史参考</span>' if archived else ''
            corpus = ' '.join([p['name'], p['role'], p['mechanism'], p['why_learn'], p['when_use'], p['limits'], *p.get('alternatives',[])])
            alt = '、'.join(p.get('alternatives', []))
            sources = ''.join(f'<a href="{E(s["url"])}">{E(s["title"])} ↗</a>' for s in p['sources'])
            intro += f'''<article id="{E(p['id'])}" class="project-card" data-role="{E(p['category'])}" data-project-search="{E(corpus)}"><div class="project-meta"><span>{E(PROJECT_CATEGORIES.get(p['category'],p['category']))}</span>{stars_html(p['stars'])}</div><h3><a href="{E(p['github_url'])}">{E(p['name'])} ↗</a></h3>{badge}<p class="project-role">{E(p['role'])}</p><p>{E(p['why_learn'])}</p><details><summary>机制、适用与取舍</summary><dl><dt>怎样工作</dt><dd>{E(p['mechanism'])}</dd><dt>适合什么情况</dt><dd>{E(p['when_use'])}</dd><dt>限制与代价</dt><dd>{E(p['limits'])}</dd><dt>可对照研究</dt><dd>{E(alt)}</dd><dt>许可范围</dt><dd><a href="{E(p['license']['source'])}">{E(p['license']['name'])} ↗</a><p>{E(p['license']['note'])}</p></dd></dl><div class="project-sources">{sources}</div></details><div class="project-bottom">{chapter_link}<a href="{E(p['docs_url'])}">官方文档 ↗</a></div><small class="snapshot">Star 快照 {E(p['stars']['as_of'])} · 来源见数值链接</small></article>'''
        intro += '''</div><p id="project-empty" hidden>没有找到匹配项目。可以清空搜索或切换到全部项目。</p><section class="reading-note"><span>这些项目怎样挑选？</span><p>结合官方文档、GitHub 关注度与技术职责选取具有代表性的项目。不同层次的项目不直接排名。许可与服务条款应按实际使用版本核对；未获取的数字明确标注。这里提供学习比较，不代替业务评测。</p><a href="resources.html">查看学习资料与整合方式 →</a></section>'''
        return intro

    def resources_page(self):
        out = '''<header class="page-heading"><p class="eyebrow">THE REFERENCE SHELF / READ THE ORIGINALS</p><h1>把好资料，<br>放到合适的章节旁。</h1><p>官方课程、原始项目与有代表性的学习资料。先读本站的中文解释，再按兴趣进入原文。</p></header><section class="reference-policy"><h2>怎样整合，而不是拼贴？</h2><p>参考课程组织、核对技术事实，用原创中文讲解与案例重新组织；每篇都保留原始资料。资料的开源代码许可不等于书籍文字或图片可任意转载。以下资源以链接导读为主，未确认许可的内容不整篇复制。</p></section><div class="resource-grid">'''
        for i,r in enumerate(self.resources):
            out += f'''<article class="resource-card" id="{E(r['id'])}"><div class="project-meta"><span>REFERENCE {i+1:02d}</span>{stars_html(r['stars'])}</div><h2><a href="{E(r['url'])}">{E(r['title'])} ↗</a></h2><div class="resource-labels"><span>{E(r['level'])}</span><span>{E(r['language'])}</span></div><p>{E(r['what_to_learn'])}</p><h3>在这本书里怎样参考</h3><p>{E(r['how_we_use'])}</p><details><summary>来源、许可与访问日期</summary><p><a href="{E(r['license']['source'])}">{E(r['license']['name'])} ↗</a></p><p>{E(r['license']['note'])}</p><p>核对日期：{E(r['verified_on'])}</p></details></article>'''
        return out + '</div><section class="reading-note"><span>阅读的顺序由问题决定</span><p>入门读者不必从头啃完英文课程或源码。先在本站目录建立结构，遇到需要更细机制的问题，再进入对应官方章节。</p><a href="map.html">返回全书目录 →</a></section>'

    def learning_guide(self):
        review = self.learning_review
        out = '''<header class="page-heading"><p class="eyebrow">AGENT FIELD GUIDE / FROM OVERVIEW TO MECHANISMS</p><h1>从一个名词，<br>读懂一套机制。</h1><p>沿 MCP、Skills、GraphRAG、ReAct 与 Harness，把概念、方法和真实执行连成深入系列。</p></header><section class="guide-intro"><h2>先分清职责，再看怎样组合</h2><div class="guide-role-grid"><a href="articles/agentic-rag-routing.html"><b>RAG</b><span>查找并组织回答依据</span></a><a href="articles/mcp-session-lifecycle.html"><b>MCP</b><span>连接有明确契约的能力</span></a><a href="articles/skills-loading.html"><b>Skills</b><span>组织可复用的任务方法</span></a><a href="articles/harness-runtime.html"><b>Harness</b><span>承载上下文与执行闭环</span></a></div><p>ReAct 是组织行动与观察的模式；上下文是当前可用信息，长期记忆需要另行管理。分层图有助于认识职责，但不是每个 Agent 都必须堆齐所有组件。</p><p>还不熟悉基础概念？先读 <a href="articles/tokens-context.html">Token 与上下文</a>、<a href="articles/prompt.html">提示词</a> 和 <a href="articles/agent.html">Agent 入门</a>，再进入下面的系列。</p></section><nav class="guide-jumps" aria-label="进阶系列快速定位">'''
        out += ''.join(f'<a href="#learn-{E(t["id"])}">{E(t["title"].split("：")[0])}</a>' for t in review['themes'])
        out += '</nav><div class="learning-series">'
        for index, topic in enumerate(review['themes']):
            existing = ' · '.join(f'<a href="articles/{slug}.html">{E(self.by_slug[slug]["title"].split("：")[0])}</a>' for slug in topic['existing'])
            lessons = ''.join(f'<li><span>{i+1:02d}</span><div><a href="articles/{slug}.html">{E(self.by_slug[slug]["title"])}</a><p>{E(self.by_slug[slug]["summary"])}</p></div></li>' for i,slug in enumerate(topic['lessons']))
            out += f'''<section class="learning-topic" id="learn-{E(topic['id'])}"><div class="learning-topic-head"><span class="part-number">{index+1:02d}</span><div><small>{E(topic['status'])}</small><h2>{E(topic['title'])}</h2><p>{E(topic['question'])}</p></div></div><p>{E(topic['summary'])}</p><div class="concept-boundary"><b>把边界讲清楚</b><p>{E(topic['correction'])}</p></div><div class="learning-prereqs"><span>已有基础</span><p>{existing}</p></div><ol class="learning-lessons">{lessons}</ol></section>'''
        out += '</div><section class="guide-questions"><p class="eyebrow">QUESTIONS THAT CONNECT THE CHAPTERS</p><h2>用八个问题，检查理解是否连起来</h2>'
        for q in review['questions']:
            out += f'<details><summary>{E(q["question"])}</summary><p>{E(q["answer"])}</p><a href="articles/{q["slug"]}.html">阅读对应章节 →</a></details>'
        sources = ' · '.join(f'<a href="{E(s["url"])}">{E(s["title"])} ↗</a>' for s in review['sources'])
        return out + f'</section><section class="reading-note"><span>从概览走向可核查的机制</span><p>本页整理学习关系，长章节给出案例、图表与具体来源。图中的层次和案例属于教学组织，实际系统按任务与约束选择组件。</p><p>{sources}</p><a href="map.html">返回全书目录 →</a></section>'
