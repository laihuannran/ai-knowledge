# AI 慢慢懂 · 图解教程书

面向零基础读者，把 AI 概念、模型机制、应用开发、主流技术栈和推理平台组织成一本可逐章阅读的中文教程。不要求编程，不设打卡进度。

**[开始阅读](https://laihuannran.github.io/ai-knowledge/)** · **[全书目录](https://laihuannran.github.io/ai-knowledge/map.html)** · [专题学习路线](https://laihuannran.github.io/ai-knowledge/guide.html) · **[技术栈图谱](https://laihuannran.github.io/ai-knowledge/stack.html)** · [参考书架](https://laihuannran.github.io/ai-knowledge/resources.html) · [全文检索](https://laihuannran.github.io/ai-knowledge/library.html)

## 书籍版（2026-11-05）

13篇、49章、128节。其中68篇为新增深入章节，每篇8–11个正文小节，结合具体机制、连贯案例、比较表与多张原创概念图。其余短文保留作为概念入口。合计264张SVG图、85张比较表与428个术语入口。

1. **先建立AI的世界地图**：任务版图、泛化与泄漏、够用的数学、神经网络学习。
2. **模型怎样读懂和生成**：Transformer、QKV、MoE、推理模型与测试时计算。
3. **模型怎样被训练出来**：数据生产、合成数据、SFT、LoRA、PPO/DPO/GRPO、训练框架、分布式训练与压缩。
4. **让回答有资料可依**：资料入库、混合检索、索引、重排、证据与拒答。
5. **从回答到执行任务**：ReAct、规划、状态、记忆、可靠执行和协作。
6. **主流应用框架怎么选**：LangChain/LangGraph系列、Agent/RAG框架、低代码与Java生态。
7. **工具协议与桌面Agent**：MCP/A2A/Skills、Codex、Claude Desktop/Code、浏览器操作与可靠执行、本地工具链。
8. **请求怎样进入模型平台**：网关、配额预算、流式事件、路由与可靠性。
9. **模型怎样高效运行**：GPU、缓存、批处理、并行、PD系列。
10. **怎样知道系统真的变好**：评测集、裁判校准、线上实验、运行与发布。
11. **文字之外的AI**：视觉、声音、视频、可控生成、一致性与实时语音Agent。
12. **把技术栈装成一套系统**：Java组件类比、场景组合和架构取舍。
13. **自我改进与递归进化研究**：改进对象、进化循环、AlphaEvolve/DGM/OpenEvolve与证据审查。

## 技术栈与资料研究

`content/research/projects.json`记录63个项目，覆盖LangChain、LangGraph、LlamaIndex、Haystack、Spring AI、LangChain4j、主流Agent框架、Dify/n8n/Flowise、Codex、Claude Code、Ollama/llama.cpp、vLLM/SGLang、LiteLLM、向量与检索数据库、Redis/Kafka、评测工具和React/AI SDK，新增scikit-learn、PyTorch、Transformers、PEFT、TRL、Datasets、TorchTitan、TorchAO、Browser Use、Diffusers、ComfyUI与LiveKit Agents。每项说明职责、机制、适用场景、限制、对照项目、许可与来源。

GitHub Star来自2026-11-04至2026-11-05的元数据快照（逐项标明日期），附来源、方法及抓取时间；无法获取明确保留空值。关注度不是品质排名。AutoGen已按官方状态标注为归档历史参考，另列接替项目。产品、源码仓库、模型权重和托管服务的授权边界分开记录。

`content/research/resources.json`包含10项学习资源，包括可核验的GitHub课程及官方课程入口。课程代码许可不自动授权复制书籍文字或图片；本站以原文链接、中文导读和原创教学整合为主，不整篇搬运不明许可内容。

## 阅读与维护

网站有可搜索、展开/收起的分篇目录；长文有本章阅读顺序、前置知识与相关章节。原有全部112篇URL保留。全文检索包含正文和比较表；图表可在手机容器内左右滑动。

仅依赖Python 3标准库：

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8765 --directory dist
```

- `content/book.json`：完整篇章结构与阅读顺序。
- `content/articles.json`、`expansion.json`、`supplement.json`：既有概念文章。
- `content/stack_chapters.json`、`deep_chapters.json`：书籍版长章节。
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
