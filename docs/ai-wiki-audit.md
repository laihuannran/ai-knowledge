# ai_wiki 技术栈差异审查

审查日期：2026-11-05。源仓库：[charliedream1/ai_wiki](https://github.com/charliedream1/ai_wiki)。固定源提交：`75529711fdc892b88cb772a727bd63bcd8ce021c`。

获取未截断递归目录，共 11,774 个条目、2,384 个 Markdown 路径；这些包含重复拷贝的文档和配套文件，不能据此声称全部都是原创文章或已经逐字审阅。此次按主题筛选和选读，不执行源仓库代码。对照基线：本书143节、63项技术栈。

## 审查结论

|处理|内容|理由|
|---|---|---|
|已有覆盖|LangChain/LangGraph、vLLM/SGLang、LiteLLM、MCP/A2A、Skills、GraphRAG、上下文与长短期记忆、RSI|继续沿用原理与专题，不重复开同名概念页|
|新增7项|MinerU、Docling、RAGFlow、Sentence Transformers、BGE/FlagEmbedding、FAISS、Chroma|补齐文档→表示→索引的具体工具链，配3篇深入教程|
|新增6项|LLaMA-Factory、Unsloth、MS-SWIFT、DeepSpeed、OpenCompass、EvalScope|连接训练工作台、计算底层与能力/性能评测，配3篇深入教程|
|新增5项|TensorRT-LLM、GPUStack、FastAPI、Gradio、Streamlit|区分引擎、资源平台、接口与界面，配3篇深入教程|
|候选，尚未展开|Agno、Parlant、CAMEL、MemOS、Cognee、EvoAgentX|有发现线索，但仍需逐项机制对照与完整专题，不能说已经写好|
|领域候选|FunASR/语音工具、PyG/DGL图神经网络、具身智能、时间序列|与已有实时语音、GraphRAG等职责不同，应独立核验和规划；目录存在不等于有充分内容|
|不优先整合|操作系统小技巧、办公软件、职业证书、育儿、副业类条目|与本次AI知识书目标关系较弱|

## 来源发现位置

以下链接固定源版本，供复查主题怎样被发现；当前技术事实另查各篇文章中的官方来源。

- [20_图像识别/04_OCR/03_转markdown/06_MinerU.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/20_%E5%9B%BE%E5%83%8F%E8%AF%86%E5%88%AB/04_OCR/03_%E8%BD%ACmarkdown/06_MinerU.md)
- [35_RAG/06_文档解析/01_文档解析/09_各类转换支持/03_docling.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/35_RAG/06_%E6%96%87%E6%A1%A3%E8%A7%A3%E6%9E%90/01_%E6%96%87%E6%A1%A3%E8%A7%A3%E6%9E%90/09_%E5%90%84%E7%B1%BB%E8%BD%AC%E6%8D%A2%E6%94%AF%E6%8C%81/03_docling.md)
- [35_RAG/18_优秀框架分析/01_ragflow.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/35_RAG/18_%E4%BC%98%E7%A7%80%E6%A1%86%E6%9E%B6%E5%88%86%E6%9E%90/01_ragflow.md)
- [06_向量数据库/10_faiss.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/06_%E5%90%91%E9%87%8F%E6%95%B0%E6%8D%AE%E5%BA%93/10_faiss.md)
- [21_NLP文本处理/10_向量模型/04_模型/01_开源模型/02_bge系列/01_bge_m3.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/21_NLP%E6%96%87%E6%9C%AC%E5%A4%84%E7%90%86/10_%E5%90%91%E9%87%8F%E6%A8%A1%E5%9E%8B/04_%E6%A8%A1%E5%9E%8B/01_%E5%BC%80%E6%BA%90%E6%A8%A1%E5%9E%8B/02_bge%E7%B3%BB%E5%88%97/01_bge_m3.md)
- [31_LLM/05_训练/04_优秀项目/02_SFT/01_LLama_factory.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/31_LLM/05_%E8%AE%AD%E7%BB%83/04_%E4%BC%98%E7%A7%80%E9%A1%B9%E7%9B%AE/02_SFT/01_LLama_factory.md)
- [31_LLM/05_训练/11_加速/02_unsloth.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/31_LLM/05_%E8%AE%AD%E7%BB%83/11_%E5%8A%A0%E9%80%9F/02_unsloth.md)
- [31_LLM/05_训练/04_优秀项目/05_通用/03_swift/01_megatron_swift.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/31_LLM/05_%E8%AE%AD%E7%BB%83/04_%E4%BC%98%E7%A7%80%E9%A1%B9%E7%9B%AE/05_%E9%80%9A%E7%94%A8/03_swift/01_megatron_swift.md)
- [31_LLM/05_训练/19_集群管理/01_GPUStack.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/31_LLM/05_%E8%AE%AD%E7%BB%83/19_%E9%9B%86%E7%BE%A4%E7%AE%A1%E7%90%86/01_GPUStack.md)
- [31_LLM/07_评估/03_评测工具/01_opencompass.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/31_LLM/07_%E8%AF%84%E4%BC%B0/03_%E8%AF%84%E6%B5%8B%E5%B7%A5%E5%85%B7/01_opencompass.md)
- [31_LLM/09_服务和部署工具/05_模型部署/02_工具/02_TensorRT_LLM/01_TensorRT_LLM.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/31_LLM/09_%E6%9C%8D%E5%8A%A1%E5%92%8C%E9%83%A8%E7%BD%B2%E5%B7%A5%E5%85%B7/05_%E6%A8%A1%E5%9E%8B%E9%83%A8%E7%BD%B2/02_%E5%B7%A5%E5%85%B7/02_TensorRT_LLM/01_TensorRT_LLM.md)
- [31_LLM/09_服务和部署工具/01_网页工具/01_tools.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/31_LLM/09_%E6%9C%8D%E5%8A%A1%E5%92%8C%E9%83%A8%E7%BD%B2%E5%B7%A5%E5%85%B7/01_%E7%BD%91%E9%A1%B5%E5%B7%A5%E5%85%B7/01_tools.md)
- [36_Agent/01_资源/02_开源框架/01_对比/03_langgraph_agno_parlant.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/36_Agent/01_%E8%B5%84%E6%BA%90/02_%E5%BC%80%E6%BA%90%E6%A1%86%E6%9E%B6/01_%E5%AF%B9%E6%AF%94/03_langgraph_agno_parlant.md)
- [36_Agent/02_原理_关键组件/06_记忆/03_MemOS.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/36_Agent/02_%E5%8E%9F%E7%90%86_%E5%85%B3%E9%94%AE%E7%BB%84%E4%BB%B6/06_%E8%AE%B0%E5%BF%86/03_MemOS.md)
- [36_Agent/02_原理_关键组件/06_记忆/07_Cognee.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/36_Agent/02_%E5%8E%9F%E7%90%86_%E5%85%B3%E9%94%AE%E7%BB%84%E4%BB%B6/06_%E8%AE%B0%E5%BF%86/07_Cognee.md)
- [36_Agent/02_原理_关键组件/08_自我进化/02_EvoAgentX.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/36_Agent/02_%E5%8E%9F%E7%90%86_%E5%85%B3%E9%94%AE%E7%BB%84%E4%BB%B6/08_%E8%87%AA%E6%88%91%E8%BF%9B%E5%8C%96/02_EvoAgentX.md)
- [14_图网络/02_原理/01_一文读懂_图卷积GNN原理_应用和库.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/14_%E5%9B%BE%E7%BD%91%E7%BB%9C/02_%E5%8E%9F%E7%90%86/01_%E4%B8%80%E6%96%87%E8%AF%BB%E6%87%82_%E5%9B%BE%E5%8D%B7%E7%A7%AFGNN%E5%8E%9F%E7%90%86_%E5%BA%94%E7%94%A8%E5%92%8C%E5%BA%93.md)
- [22_音频/02_语音识别/04_工具/02_funASR/01_使用/01_SDK使用及部署说明.md](https://github.com/charliedream1/ai_wiki/blob/75529711fdc892b88cb772a727bd63bcd8ce021c/22_%E9%9F%B3%E9%A2%91/02_%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB/04_%E5%B7%A5%E5%85%B7/02_funASR/01_%E4%BD%BF%E7%94%A8/01_SDK%E4%BD%BF%E7%94%A8%E5%8F%8A%E9%83%A8%E7%BD%B2%E8%AF%B4%E6%98%8E.md)

## 版本与证据说明

- 根目录README带Apache 2.0标识，本次固定提交根目录未见独立LICENSE文件，不能把徽章当成对所有第三方摘录、图片和链接文章的完整授权；本站只保留发现链接并原创重写。
- Agno/Parlant对比条目含图片及外部文章入口，不能仅凭该条目认定当前框架功能。
- MemOS笔记含2025年尚待开源的时点描述，不能不加区分移入2026年教程。
- EvoAgentX旧仓库地址目前重定向至ANative-Lab/EvoAgentX，已有RSI系列的评价框架仍适用，未把“工作流优化”改写为无界自我改进。
- GitHub REST元数据遇到限流，未取得的新项目Star明确空值，不以网页近似显示或旧笔记数字填充。许可可从官方许可文本另行核对，不能由Star请求失败推断许可。
- 尚未实跑工具和模型，本次产物属于文档研究与教学整理，不是性能测评或线上兼容认证。
