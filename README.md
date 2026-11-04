# AI 慢慢懂 · 图解知识库

写给零基础、希望随时翻阅 AI 知识的读者。不要求编程，不设学习进度。

**[进入阅读站](https://laihuannran.github.io/ai-knowledge/)** · [知识地图](https://laihuannran.github.io/ai-knowledge/map.html) · [术语速查](https://laihuannran.github.io/ai-knowledge/glossary.html)

八个专题、20 篇原创入门讲解、20 张 SVG 概念图、71 个术语入口。每篇包括生活类比、图解、概念解释、场景、误区、自测解释与官方资料。

## 阅读目录

1. AI 基础：AI 地图、训练与推理、Token/上下文/幻觉。
2. 模型能力：Transformer/Attention/MoE、多模态与模型交付方式。
3. AI 应用：提示词、RAG、RAG 与微调的选择。
4. 智能体：Agent 与工作流、MCP/API/Skill。
5. 接入平台：推理网关、智能路由与负载均衡。
6. 推理设施：GPU 与量化、KV Cache、PD 分离、推理引擎与集群。
7. 评测运行：大模型评测、性能与成本、可观测性与安全。
8. 行业技术栈：产品职责、代表项目、选型问题。

也可在 [content](content) 中直接阅读 Markdown 文章。模型路由、RAG、PD 等技术按概念说明，不承诺特定厂商性能或固定版本能力。示意图是简化模型，案例数字是教学假设。

## 来源与时效

各篇文末附官方文档或项目链接；初始整理日期为 2026-11-04。`content/source-checks.json` 记录链接 HTTP 检查结果，可达不代表对页面所有内容作出背书。文字为原创综合解释，不是官方文档翻译或转载。此项目没有定时采集任务，内容更新通过后续提交完成。

## 本地构建（维护者可选，读者无需操作）

仅依赖 Python 3 标准库：

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8765 --directory dist
```

打开 `http://localhost:8765`。`content/articles.json` 是正文数据源，`scripts/build.py` 生成网页、Markdown 和 SVG；`assets` 存放样式及搜索逻辑。`seed_content.py` 仅用于重建初始数据，日常编辑请直接修改 JSON，避免覆盖已有更新。

## GitHub Pages

仓库 Settings → Pages → Build and deployment 的 Source 选择 **GitHub Actions**。推送 `main` 后，工作流构建并部署 `dist`。所有站内链接采用相对地址，支持 `/ai-knowledge/` 项目路径。`dist` 一并保留便于直接查看和迁移。

## 许可

原创文字与 SVG 示意图： [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hans)。
构建代码和页面样式：MIT，见 [LICENSE](LICENSE)。第三方资料归原作者，遵循其各自许可。
