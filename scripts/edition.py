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
    'ml': '机器学习基础', 'training': '训练与模型优化', 'browser': '浏览器与电脑操作',
    'generative': '多模态生成', 'realtime': '实时语音交互',
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
    'A2A': 'a2a-discovery', 'Darwin Gödel Machine': 'rsi-research-cases', 'OpenEvolve': 'rsi-evolution-loop',
    'Microsoft GraphRAG': 'graphrag-indexing', 'LightRAG': 'graphrag-querying',
    'Graphiti': 'long-term-memory-recall', 'Mem0': 'long-term-memory-write', 'Letta': 'short-term-memory',
    'Anthropic Skills 示例': 'skills-loading', 'Agent Skills 规范': 'skills-loading',
    'Neo4j': 'graphrag-indexing',
    'scikit-learn': 'ml-task-map', 'PyTorch': 'neural-learning',
    'Transformers': 'training-framework-stack', 'PEFT': 'training-framework-stack',
    'TRL': 'dpo-grpo', 'Datasets': 'data-production',
    'TorchTitan': 'distributed-training', 'TorchAO': 'model-compression',
    'Browser Use': 'browser-computer-agents', 'Diffusers': 'image-generation-control',
    'ComfyUI': 'image-generation-control', 'LiveKit Agents': 'realtime-voice-agent',
    'MinerU': 'wiki-document-stack', 'Docling': 'wiki-document-stack', 'RAGFlow': 'wiki-document-stack',
    'Sentence Transformers': 'wiki-embedding-stack', 'FlagEmbedding': 'wiki-embedding-stack',
    'FlagEmbedding（BGE）': 'wiki-embedding-stack', 'FAISS': 'wiki-vector-stack', 'Chroma': 'wiki-vector-stack',
    'LLaMA-Factory': 'wiki-finetuning-workbenches', 'Unsloth': 'wiki-finetuning-workbenches',
    'MS-SWIFT': 'wiki-finetuning-workbenches', 'DeepSpeed': 'wiki-deepspeed-stack',
    'OpenCompass': 'wiki-evaluation-workbenches', 'EvalScope': 'wiki-evaluation-workbenches',
    'TensorRT-LLM': 'wiki-serving-engines', 'GPUStack': 'wiki-gpu-platform',
    'FastAPI': 'wiki-ai-interface-stack', 'Gradio': 'wiki-ai-interface-stack', 'Streamlit': 'wiki-ai-interface-stack',
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
        self.beginner_groups = self.book.get('beginner_route', [])
        self.beginner_slugs = [slug for group in self.beginner_groups for slug in group['slugs']]
        self.learning_review = read_json('content/learning_review.json', {'themes': [], 'questions': [], 'sources': []})
        self.series_count = len({slug for t in self.learning_review['themes'] for slug in t['lessons']})
        self.projects = read_json('content/research/projects.json', [])
        self.resources = read_json('content/research/resources.json', [])
        self.api_protocols = read_json('content/api_protocols.json', {'date': '', 'profiles': [], 'extensions': []})
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
            tag = '小白主线' if slug in self.beginner_slugs else ('机制与案例' if level == '深入' else '概念入门')
            content_len = sum(len(s['text']) for s in a['sections'])
            mins = max(3, math.ceil(content_len / 240))
            summary = '' if compact else f'<p>{E(a["summary"])}</p>'
            items.append(f'''<li data-book-search="{E(a['title']+' '+a['summary']+' '+' '.join(a['tags']))}"><span class="toc-index">{i+1:02d}</span><div><a href="articles/{slug}.html">{E(a['title'])}</a>{summary}</div><span class="depth-badge {'deep' if level=='深入' else ''}">{tag}<small>{mins} 分钟</small></span></li>''')
        return '<ol class="chapter-reading">' + ''.join(items) + '</ol>'

    def reading_stages(self):
        by_id = {part['id']: part for part in self.parts}
        cards = []
        for index, stage in enumerate(self.book.get('stages', [])):
            links = ' · '.join(f'<a href="map.html#{E(key)}">{E(by_id[key]["title"])}</a>' for key in stage['parts'])
            cards.append(f'<section><small>阶段 {index+1:02d}</small><h3>{E(stage["title"])}</h3><p>{E(stage["goal"])}</p><div>{links}</div></section>')
        return '<section class="reading-stages" aria-label="从浅到深的四个学习阶段">' + ''.join(cards) + '</section>'

    def beginner_route(self, compact=False):
        count = len(self.beginner_slugs)
        out = f'<section class="beginner-route guide-intro" id="beginner-route"><p class="eyebrow">START HERE / ZERO CODING REQUIRED</p><h2>第一次读，沿这 {count} 节小白主线走。</h2><p>先建立能串起来的概念，不要求编程或打卡。主线会跳过各主题的深入细节；读完以后，再沿完整目录逐层补充。每次读一节也可以，文末有连续阅读入口。</p>'
        if compact:
            out += '<p>' + ' → '.join(E(group['title']) for group in self.beginner_groups) + '</p><a class="primary-link" href="guide.html#beginner-route">查看逐节阅读顺序 →</a>'
        else:
            offset = 0
            for group in self.beginner_groups:
                lessons = ''.join(f'<li><span>{offset+i+1:02d}</span><div><a data-beginner-lesson="{E(slug)}" href="articles/{slug}.html">{E(self.by_slug[slug]["title"])}</a></div></li>' for i,slug in enumerate(group['slugs']))
                out += f'<section id="{E(group["id"])}" class="beginner-group"><h3>{E(group["title"])}</h3><p>{E(group["goal"])}</p><ol class="learning-lessons">{lessons}</ol></section>'
                offset += len(group['slugs'])
            out += '<p>读完主线：先扩展多模态和感兴趣的应用，再进入模型内部与工程深入。训练和 RSI 可以最后读。</p><a class="primary-link" href="map.html">按完整目录继续深入 →</a>'
        return out + '</section>'

    def beginner_navigation(self, slug):
        if slug not in self.beginner_slugs:
            return ''
        index = self.beginner_slugs.index(slug)
        if index+1 < len(self.beginner_slugs):
            following = self.beginner_slugs[index+1]
            action = f'<a data-beginner-next="{E(following)}" href="{following}.html">主线下一节 →<br><b>{E(self.by_slug[following]["title"])}</b></a>'
        else:
            action = '<a href="../map.html#multimodal">主线读完了，继续扩展应用 →</a>'
        return f'<nav class="beginner-navigation" aria-label="小白主线连续阅读"><div><small>小白主线 · 第 {index+1} / {len(self.beginner_slugs)} 节</small><p>沿概念关系继续，深入细节可以稍后再读。</p><a href="../guide.html#beginner-route">返回主线目录</a></div>{action}</nav>'

    def home(self):
        chapters = sum(len(p['chapters']) for p in self.parts)
        cover = '''<div class="book-display" aria-label="AI慢慢懂图解教程封面"><div class="book-cover"><div class="cover-kicker">A FIELD GUIDE TO ARTIFICIAL INTELLIGENCE</div><h2>AI<br>慢慢懂</h2><div class="cover-line"></div><p>从概念，到系统。<br>从模型，到技术栈。</p><span class="cover-mark">图解教程 · 书籍版</span><small>HUANRAN’S LEARNING LIBRARY / 2026</small></div><div class="book-caption">一本可以按顺序读，也可以带着问题翻的书。</div></div>'''
        hero = f'''<section class="book-hero"><div><p class="eyebrow">THE AI LEARNING LIBRARY / BOOK EDITION</p><h1>把 AI，<br>学成<span>一套知识。</span></h1><p class="book-lead">先用例子听懂概念，再学会提问、查资料与理解 Agent。<br>无需先会编程，跟着 {len(self.beginner_slugs)} 节主线，一层一层读懂。</p><div class="hero-actions"><a class="primary-link" href="guide.html#beginner-route">按小白主线开始 <span>→</span></a><a class="quiet-link" href="map.html">展开完整目录 ↗</a></div><div class="book-stats"><span><b>{len(self.parts):02d}</b>篇</span><span><b>{chapters}</b>章</span><span><b>{self.deep_count}</b>篇深入讲解</span></div></div>{cover}</section>'''
        routes = '<section class="entry-routes"><a href="guide.html#beginner-route"><small>READ IN ORDER</small><h3>沿小白主线读</h3><p>按概念关系，逐节建立理解。</p><span>查看主线目录 →</span></a><a href="map.html"><small>GO DEEPER</small><h3>沿完整目录深入</h3><p>回到感兴趣的主题，继续读机制与案例。</p><span>展开全书目录 →</span></a><a href="stack.html"><small>LOOK UP A TOOL</small><h3>按工具查阅</h3><p>已经遇到具体项目时，查职责、机制与取舍。</p><span>打开技术栈图谱 →</span></a></section>'

        toc = '<section class="book-overview"><div class="section-head"><div><p class="eyebrow">CONTENTS / FROM THE FIRST PRINCIPLE TO THE STACK</p><h2>这本书，怎样展开？</h2></div><a class="quiet-link" href="map.html">展开完整目录 →</a></div><div class="part-grid">'
        for i,p in enumerate(self.parts):
            count = sum(len(c['slugs']) for c in p['chapters'])
            chapter_names = ' / '.join(c['title'] for c in p['chapters'])
            toc += f'''<a class="part-card" href="map.html#{E(p['id'])}"><span class="part-number">{i+1:02d}</span><div><small>{E(p['subtitle'])}</small><h3>{E(p['title'])}</h3><p>{E(p['description'])}</p><span class="part-meta">{len(p['chapters'])} 章 · {count} 节 <b>↗</b></span><span class="visually-hidden">{E(chapter_names)}</span></div></a>'''
        toc += '</div></section>'
        stack = f'''<section class="stack-teaser"><p class="eyebrow">A MAP OF THE AI ECOSYSTEM</p><h2>不只认识名词，<br>还要知道工具放在哪里。</h2><p>研究 {len(self.projects)} 个项目，按机器学习、训练、Agent、生成、数据、网关、推理与评测分类。<br>每项都解释职责、机制、适用场景、限制和许可；GitHub 关注度附采集日期。</p><div class="stack-name-row"><span>LangChain</span><span>LangGraph</span><span>Spring AI</span><span>Codex</span><span>vLLM</span><span>Redis</span></div><a class="primary-link" href="stack.html">查看技术栈与比较 <span>→</span></a></section>'''
        note = f'''<section class="reading-note"><span>这是一份怎样的教程？</span><p>{len(self.articles)} 节内容区分概念入门与机制案例。每篇先直接解释、再举例和分步讲机制，文末留下一句核心。新术语随文说明，深入章节保留图表与原始资料。</p><a href="resources.html">查看参考书架与资料来源 →</a></section>'''
        return hero + self.beginner_route(compact=True) + self.reading_stages() + routes + toc + stack + note

    def contents(self):
        out = f'''<header class="page-heading"><p class="eyebrow">TABLE OF CONTENTS / READ LIKE A BOOK</p><h1>从第一篇，<br>读到一套完整架构。</h1><p>{len(self.parts)} 篇 · {sum(len(p['chapters']) for p in self.parts)} 章 · {len(self.articles)} 节。先走小白主线，再在同一主题下补机制与案例；完整目录中每篇前置知识均位于更早位置。</p></header>''' + self.beginner_route(compact=True) + self.reading_stages() + '''<div class="contents-tools"><label class="search"><span>⌕</span><input id="book-search" type="search" placeholder="在目录中找 A2A、RSI、RAG、PD…" aria-label="搜索全书目录"></label><button id="expand-toc" type="button">展开全部篇章</button><button id="collapse-toc" type="button">收起全部篇章</button></div><p id="book-results" class="result-count" aria-live="polite">按知识前置关系排列 · “小白主线”标记可先读</p><div class="book-contents">'''
        for i,p in enumerate(self.parts):
            chapters = ''
            for j,c in enumerate(p['chapters']):
                chapters += f'''<section id="{E(c['id'])}" class="book-chapter"><div class="chapter-heading"><span>第 {j+1:02d} 章</span><h3>{E(c['title'])}</h3></div><p class="chapter-summary">{E(c['summary'])}</p>{self.chapter_list(c)}</section>'''
            out += f'''<details class="book-part" id="{E(p['id'])}" open><summary><span class="part-number">{i+1:02d}</span><div><small>{E(p['subtitle'])}</small><h2>{E(p['title'])}</h2><p>{E(p['description'])}</p></div><span class="part-toggle" aria-hidden="true">＋</span></summary>{chapters}</details>'''
        out += '</div><p id="book-empty" hidden>没有找到对应章节。可尝试术语别名，或使用文章全文搜索。</p><section class="reading-note"><span>想按问题查阅？</span><p>目录搜索用于定位章节；文章检索会同时搜索正文、术语与比较表。</p><a href="library.html">打开全文检索 →</a></section>'
        return out

    def stack(self):
        categories = list(dict.fromkeys(p['category'] for p in self.projects))
        intro = f'''<header class="page-heading"><p class="eyebrow">THE AI STACK ATLAS / DATED GITHUB SNAPSHOTS</p><h1>优秀工具很多，<br>先看它们各管哪一层。</h1><p>{len(self.projects)} 个项目的职责、机制与取舍。GitHub Star 是关注度快照，逐项标注采集日期，不代表本教程的品质排名。</p></header><section class="architecture-strip" aria-label="技术栈分层"><a href="#project-list" data-role-shortcut="ml,training">学习与训练</a><span>↔</span><a href="#project-list" data-role-shortcut="generative,realtime,browser">生成与交互</a><span>↔</span><a href="#project-list" data-role-shortcut="frontend,client">交互与客户端</a><span>→</span><a href="#project-list" data-role-shortcut="appframeworks,agents,lowcode">应用与 Agent</a><span>→</span><a href="#project-list" data-role-shortcut="data">数据与检索</a><span>→</span><a href="#project-list" data-role-shortcut="gateway,serving">网关与推理</a><span>↔</span><a href="#project-list" data-role-shortcut="eval">评测与运行</a></section><div class="stack-guide"><p>先用技术栈专章理解架构，再查项目细节：<a href="articles/stack-langchain.html">LangChain</a> · <a href="articles/stack-langgraph-state.html">LangGraph</a> · <a href="articles/stack-agent-frameworks.html">Agent 框架比较</a> · <a href="articles/stack-codex.html">Codex</a> · <a href="articles/stack-claude.html">Claude</a> · <a href="articles/deep-stack-architecture.html">完整技术栈案例</a></p></div><div class="section-head" id="project-list"><h2>按职责找工具</h2><label class="search"><span>⌕</span><input id="project-search" type="search" placeholder="查找项目、机制、适用场景…" aria-label="搜索技术项目"></label></div><div class="project-filters filters"><button class="active" data-project-filter="all" aria-pressed="true">全部项目</button>'''
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
        out = '<header class="page-heading"><p class="eyebrow">READ IN ORDER / THEN GO DEEPER</p><h1>先走一条主线，<br>再把知识逐层展开。</h1><p>零基础从下方主线开始；读过概念以后，再按完整目录或专题继续深入。无需先学训练、数学和部署。</p></header>'
        out += self.beginner_route() + self.reading_stages()
        out += '<section class="guide-intro"><h2>主线之后，按问题深入专题</h2><p>下面的专题按全书首次出现的位置排列，各专题内部也按目录顺序阅读。一个专题可能跨越应用与工程阶段；先读每篇标注的前置知识，不必一口气读完全部系列。</p><a href="map.html">查看完整章节与前置关系 →</a></section><nav class="guide-jumps" aria-label="进阶系列快速定位">'
        out += ''.join(f'<a href="#learn-{E(t["id"])}">{E(t["title"].split("：")[0])}</a>' for t in review['themes'])
        out += '</nav><div class="learning-series">'
        for index, topic in enumerate(review['themes']):
            existing = ' · '.join(f'<a href="articles/{slug}.html">{E(self.by_slug[slug]["title"].split("：")[0])}</a>' for slug in topic['existing'])
            lessons = ''.join(f'<li><span>{i+1:02d}</span><div><a href="articles/{slug}.html">{E(self.by_slug[slug]["title"])}</a><p>{E(self.by_slug[slug]["summary"])}</p></div></li>' for i,slug in enumerate(topic['lessons']))
            out += f'''<section class="learning-topic" id="learn-{E(topic['id'])}"><div class="learning-topic-head"><span class="part-number">{index+1:02d}</span><div><small>{E(topic['status'])}</small><h2>{E(topic['title'])}</h2><p>{E(topic['question'])}</p></div></div><p>{E(topic['summary'])}</p><div class="concept-boundary"><b>容易混淆的地方</b><p>{E(topic['correction'])}</p></div><div class="learning-prereqs"><span>这些概念还不熟，可以先看</span><p>{existing}</p></div><ol class="learning-lessons">{lessons}</ol></section>'''
        out += '</div><section class="guide-questions"><p class="eyebrow">QUESTIONS THAT CONNECT THE CHAPTERS</p><h2>用具体问题，检查理解是否连起来</h2>'
        for q in review['questions']:
            out += f'<details><summary>{E(q["question"])}</summary><p>{E(q["answer"])}</p><a href="articles/{q["slug"]}.html">阅读对应章节 →</a></details>'
        sources = ' · '.join(f'<a href="{E(s["url"])}">{E(s["title"])} ↗</a>' for s in review['sources'])
        return out + f'</section><section class="reading-note"><span>从概览走向可核查的机制</span><p>本页整理学习关系，长章节给出案例、图表与具体来源。图中的层次和案例属于教学组织，实际系统按任务与约束选择组件。</p><p>{sources}</p><a href="map.html">返回全书目录 →</a></section>'


    def api_reference(self):
        data = self.api_protocols
        labels = {'model': '模型 API', 'cloud': '云平台接入', 'agent': '代理与客户端接线'}
        rows, cards, jumps = [], [], []
        for item in data['profiles']:
            key = E(item['id'])
            terms = E(' '.join(str(item[k]) for k in ('name','kind','endpoint','input','output','stream','tools','state','auth','limit')).lower())
            jumps.append(f'<a href="#api-{key}" data-api-search="{terms}">{E(item["name"])}</a>')
            cols = [f'<a href="#api-{key}">{E(item["name"])}</a><small>{E(labels[item["kind"]])}</small>']
            cols += [E(item[k]) for k in ('input','output','stream','tools','state')]
            rows.append(f'<tr data-api-search="{terms}">' + ''.join(f'<td>{value}</td>' for value in cols) + '</tr>')
            source_links = ' · '.join(f'<a href="{E(source["url"])}">{E(source["title"])} ↗</a>' for source in item['sources'])
            fields = ''.join(f'<dt>{label}</dt><dd>{E(item[field])}</dd>' for label,field in [('输入','input'),('输出','output'),('流式交付','stream'),('工具循环','tools'),('会话与状态','state'),('鉴权与范围','auth')])
            cards.append(f'<article class="api-profile" id="api-{key}" data-api-search="{terms}"><div class="project-meta"><span>{E(labels[item["kind"]])}</span><span>核对 {E(data["date"])}</span></div><h2>{E(item["name"])}</h2><p class="api-endpoint"><code>{E(item["endpoint"])}</code></p><dl>{fields}</dl><div class="concept-boundary"><b>适配时保留的边界</b><p>{E(item["limit"])}</p></div><p class="api-sources">{source_links}</p><a class="api-read" href="articles/{E(item["chapter"])}.html">阅读机制与案例 →</a></article>')
        extensions = ''.join(f'<article><h3><a href="{E(item["url"])}">{E(item["name"])} ↗</a></h3><p>{E(item["note"])}</p></article>' for item in data['extensions'])
        return f'''<header class="page-heading"><p class="eyebrow">MODEL API ATLAS / CONTRACTS AND COMPATIBILITY</p><h1>同样在调用模型，<br>契约未必相同。</h1><p>把接口、模型、平台与客户端分开，按请求、事件、工具和状态核对。资料核对日期：{E(data['date'])}。以下是概念对照与文档研究，未进行付费调用或线上兼容性实测。</p></header><section class="guide-intro"><h2>先分三类，再看字段</h2><div class="guide-role-grid"><a href="articles/api-protocol-map.html"><b>模型 API</b><span>Chat、Responses、Messages 与 Gemini</span></a><a href="articles/api-bedrock-families.html"><b>云接入</b><span>Bedrock 的端点、鉴权和接口族</span></a><a href="articles/api-kiro-boundaries.html"><b>代理接线</b><span>Kiro 产品、ACP、MCP 与模型接口</span></a></div><p>本页所说“协议”包含厂商 API 契约，并不表示它们都是开放行业标准。OpenAI-compatible 表示具体范围内的兼容；SDK能连接、文本能返回，都不能证明工具、多模态、状态与参数完全等价。</p><a class="primary-link" href="guide.html#learn-model-apis">按顺序阅读九篇协议教程 →</a></section><nav class="guide-jumps" aria-label="接口快速定位">{''.join(jumps)}</nav><div class="section-head"><h2>按能力与字段查阅</h2><label class="search"><span>⌕</span><input id="api-search" type="search" placeholder="例如 Responses、SSE、工具、SigV4…" aria-label="搜索模型 API 对照"></label></div><p id="api-results" class="result-count" aria-live="polite">共 {len(data['profiles'])} 种接入形态，按职责对照</p><div class="table-scroll api-table" role="region" aria-label="API契约比较，可左右滚动" tabindex="0"><table><thead><tr><th scope="col">接入形态</th><th scope="col">输入</th><th scope="col">输出</th><th scope="col">流式</th><th scope="col">工具</th><th scope="col">状态</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div><p id="api-empty" hidden>没有找到对应项，可尝试厂商名称、字段名或能力关键词。</p><div class="api-profile-grid">{''.join(cards)}</div><section class="api-extensions"><p class="eyebrow">RELATED ACCESS PATHS</p><h2>还会遇到的接入形态</h2><p>这些入口继续按自己的提供商文档核对，不由某条兼容路径推断整个生态。</p><div>{extensions}</div></section><section class="reading-note"><span>比较的是语义，不只是改字段名</span><p>能力矩阵应区分文档声明、离线回放、线上实测与业务验收。不支持的能力要明确拒绝或说明降级，不能静默删除。原始调用身份、不透明状态、模态与结束原因都可能影响后续行为。</p><a href="articles/api-compatibility-testing.html">阅读兼容性验收 →</a></section>'''
