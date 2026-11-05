# AI 慢慢懂 · 图解教程书

面向零基础读者，把 AI 概念、模型机制、应用开发、主流技术栈和推理平台组织成一本可逐章阅读的中文教程。不要求编程，不设打卡进度。

**[开始阅读](https://laihuannran.github.io/ai-knowledge/)** · **[全书目录](https://laihuannran.github.io/ai-knowledge/map.html)** · [专题学习路线](https://laihuannran.github.io/ai-knowledge/guide.html) · [模型 API 对照](https://laihuannran.github.io/ai-knowledge/api.html) · **[技术栈图谱](https://laihuannran.github.io/ai-knowledge/stack.html)** · [参考书架](https://laihuannran.github.io/ai-knowledge/resources.html) · [全文检索](https://laihuannran.github.io/ai-knowledge/library.html)

## 书籍版（2026-11-05）

14篇、61章、153节。其中93篇为新增深入章节，每篇8–11个正文小节，结合具体机制、连贯案例、比较表与多张原创概念图。其余短文保留作为概念入口。合计339张SVG图、112张比较表与522个术语入口。

先沿 **[28节小白主线](https://laihuannran.github.io/ai-knowledge/guide.html#beginner-route)** 阅读：概念与提问 → 知识库与证据 → Agent与记忆 → 工具和产品 → 主流框架。每篇主线文章有专用“主线下一节”，与完整目录翻页分别标明。

完整目录按四阶段展开，所有250条前置知识关系均指向更早的文章：

1. **先听懂AI，再学会提问**：模型、Token、提示、评测与资料质量。
2. **让AI查资料后再回答**：文档、召回、重排、证据、具体工具链与GraphRAG。
3. **让AI从回答走向做事**：Agent、ReAct、计划、状态、上下文与长短期记忆。
4. **认识工具、技能与Agent产品**：MCP/Skills、Codex/Claude、本地客户端、浏览器、A2A与Agentic RAG。
5. **把概念对应到主流技术栈**：生态地图、LangChain/LangGraph、RAG/Agent框架、低代码与应用界面。
6. **让AI看图、听声音和理解视频**：视觉、语音、生成、交互与多模态案例。
7. **回到模型内部：答案怎样生成**：概率、采样、Transformer、QKV与推理时计算。
8. **让模型在硬件上高效运行**：显存、计算阶段、性能、缓存、批处理、多卡、引擎与PD。
9. **深入评测与线上运行**：裁判、评测集、工作台、实验、灰度与回滚。
10. **请求怎样进入模型平台**：网关、配额、流式事件、智能路由与可靠性。
11. **模型API与协议兼容**：Chat/Responses/Messages、Gemini、Bedrock、Kiro与兼容验收。
12. **模型怎样学习、微调和对齐**：梯度、数据、SFT、LoRA、强化学习、训练框架与DeepSpeed。
13. **把所有知识连成可交付系统**：架构、恢复与交接、Harness、安全和企业案例。
14. **自我改进与递归进化研究**：改进对象、循环、研究案例与证据审查。

`content/book.json`统一维护篇章、四个学习阶段与28节主线，首页、目录、导览和文章导航都由它生成。原153篇文章地址与73个既有篇章锚点保持可用；数学与训练机制后置，工具章节接在对应原理之后。

## 技术栈与资料研究

`content/research/projects.json`记录81个项目，覆盖LangChain、LangGraph、LlamaIndex、Haystack、Spring AI、LangChain4j、主流Agent框架、Dify/n8n/Flowise、Codex、Claude Code、Ollama/llama.cpp、vLLM/SGLang、LiteLLM、向量与检索数据库、Redis/Kafka、评测工具和React/AI SDK，新增scikit-learn、PyTorch、Transformers、PEFT、TRL、Datasets、TorchTitan、TorchAO、Browser Use、Diffusers、ComfyUI与LiveKit Agents。每项说明职责、机制、适用场景、限制、对照项目、许可与来源。

GitHub Star来自2026-11-04至2026-11-05的元数据快照（逐项标明日期），附来源、方法及抓取时间；无法获取明确保留空值。关注度不是品质排名。AutoGen已按官方状态标注为归档历史参考，另列接替项目。产品、源码仓库、模型权重和托管服务的授权边界分开记录。

`content/research/resources.json`包含11项学习资源，包括可核验的GitHub课程及官方课程入口。课程代码许可不自动授权复制书籍文字或图片；本站以原文链接、中文导读和原创教学整合为主，不整篇搬运不明许可内容。

模型API对照页使用 `content/api_protocols.json` 记录9种接入形态，区分模型接口、云端接口族与Kiro代理接线，按输入、输出、流式、工具、状态、鉴权和限制查阅；附Azure OpenAI、DeepSeek和Model Studio等官方扩展入口。这是文档研究与教学整理，不是线上兼容性认证。

本次对照 [ai_wiki](https://github.com/charliedream1/ai_wiki) 补入18项具体工具与9篇深入教程，另加[差异导览](https://laihuannran.github.io/ai-knowledge/articles/wiki-curation-map.html)。覆盖文档解析、BGE/嵌入、FAISS/Chroma、微调工作台、DeepSpeed、TensorRT-LLM、GPUStack、界面服务和评测工作台。发现位置、已有覆盖与候选领域记录在 [差异审查](docs/ai-wiki-audit.md)。新项目Star因API限流保留空值；18项许可证另从官方文本核对，MinerU附加条款单独标明。

## 通俗讲解版

全书按“先直接说明 → 举例 → 分步骤解释 → 一句话记住”组织。技术术语保留用于查阅，首次出现时尽量随文说明，不默认读者懂编程。参数不是保存文本的格子，输入图片不等于能精确读懂所有细节等常见误解，已写入对应基础章节。

`plain_intro` 是文章开头的直接解释，`takeaway` 是文末的一句核心；两者同步进入网页、GitHub Markdown 与全文检索。正文逐篇重新讲解，深入章节仍保留机制、限制、比较表与多张图。引用和技术核对日期与表达修订分开理解：通俗化不等于重新测评了全部产品。

## 阅读与维护

网站有可搜索、展开/收起的分篇目录；长文有本章阅读顺序、前置知识与相关章节。原有全部143篇URL保留。全文检索包含正文和比较表；图表可在手机容器内左右滑动。

仅依赖Python 3标准库：

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8765 --directory dist
```

- `content/wiki_curation.json`、`wiki_retrieval_series.json`、`wiki_training_series.json`、`wiki_serving_series.json`：ai_wiki差异导览与九篇具体工具链教程。
- `content/book.json`：完整篇章结构与阅读顺序。
- `content/articles.json`、`expansion.json`、`supplement.json`：既有概念文章。
- `content/stack_chapters.json`、`deep_chapters.json`：书籍版长章节。
- `content/api_protocols.json`：模型API矩阵；`openai_api_series.json`、`claude_gemini_api_series.json`、`cloud_client_api_series.json`、`api_adapter_series.json`：九篇协议与适配深入教程。
- `content/context_series.json`、`memory_series.json`：上下文组装/压缩/评测、短期状态与长期记忆写入/召回。
- `content/foundation_series.json`、`reasoning_series.json`、`data_training_series.json`、`interactive_multimodal_series.json`：基础、推理强化学习、数据训练、浏览器与生成交互系列。
- `content/protocol_landscape.json`、`a2a_series.json`、`rsi_series.json`：协议地图、A2A与递归自我改进系列。
- `content/protocol_series.json`、`retrieval_series.json`、`agent_series.json`：MCP/Skills、进阶RAG、Agent运行系列。
- `content/learning_review.json`：Agent进阶路线与概念边界。
- `content/*.md`：构建生成的GitHub阅读版文章。
- `scripts/edition.py`：书籍导览、项目图谱和参考书架。
- `scripts/diagrams.py`：原创SVG概念图。
- `assets/`：样式和浏览器搜索交互。

编辑结构化内容后运行构建，勿手工修改生成的`dist`或Markdown。`seed_content.py`仅用于首批原始数据重建，不应用来覆盖后续编辑。`check_sources.py`记录HTTP可达情况；网络失败不自动等于链接失效，人工概念核验另行记录。

## 发布与边界

Settings → Pages → Source选择GitHub Actions。推送`main`后工作流构建并发布`dist`。所有站内链接支持项目路径。当前没有设置自动采集或定时生成文章。

这是一份逐步深化的教程，不宣称包含全部AI知识；入门图示有意简化，假设数字不代表实测性能或厂商报价。具体产品能力和许可应以所选版本的原始资料为准。

## 许可

原创文字与SVG图采用[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hans)，构建代码与样式采用MIT，见[LICENSE](LICENSE)。链接资料归原作者，遵循其各自许可。

## Agent进阶系列（2026-11-05）

**[从一个名词读懂一套机制](https://laihuannran.github.io/ai-knowledge/guide.html)**：8个学习主题连接18篇新增长章节，补齐独立MCP、Skills、GraphRAG、Agentic RAG、Harness与企业案例。ReAct、上下文和记忆在原有章节基础上继续深入。

把概览图作为选题线索，逐项核对标准与产品实现。七层图不是唯一标准；MCP不自动连通全部工具，Skills不等于模型训练或权限授予，上下文也不等于永久保留全部聊天。案例为原创教学设计，未公开用户截图或个人水印信息。

项目图谱新增Microsoft GraphRAG、LightRAG、Graphiti、Mem0、Letta、Agent Skills规范与示例、Neo4j；新条目逐项记录Star快照日期与许可来源，不将关注度当作质量排名。
