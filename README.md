# AI 慢慢懂 · 图解知识库

写给零基础、希望随时翻阅 AI 知识的读者。不要求编程，不设学习进度。

**[进入阅读站](https://laihuannran.github.io/ai-knowledge/)** · [知识地图](https://laihuannran.github.io/ai-knowledge/map.html) · [术语速查](https://laihuannran.github.io/ai-knowledge/glossary.html)

10 个专题、60 篇原创讲解、60 张 SVG 概念图、17 张比较表、219 个术语入口。每篇包括生活类比、图解、概念解释、场景、误区、自测解释与官方资料。

## 阅读目录

1. AI 基础：AI 地图、训练与推理、Token/上下文/幻觉、损失梯度、向量与概率。
2. 模型能力：Transformer/Attention/MoE、QKV与位置、采样解码、模型交付方式。
3. 训练与对齐：数据质量、SFT、LoRA/QLoRA、偏好优化与蒸馏。
4. AI 应用：提示词、RAG、文档解析、混合检索/RRF、重排、向量索引、证据与拒答。
5. 智能体：Agent、MCP/API/Skill、记忆、计划、工具可靠性、多智能体协作。
6. 接入平台：网关、路由、配额预算、重试熔断、缓存路由、流式事件。
7. 推理设施：GPU/量化、KV Cache、PD分离、批处理、推测解码、并行与性能瓶颈。
8. 评测运行：评测集、检索指标、裁判校准、A/B、可观测性、灰度回归与回滚。
9. 多模态：视觉/OCR、ASR/TTS、扩散图像生成、视频理解。
10. 行业技术栈：产品职责、代表项目、云端/本地/混合方案的判断依据。

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

打开 `http://localhost:8765`。`content/articles.json`、`content/expansion.json`、`content/supplement.json` 是正文数据源，`scripts/build.py` 生成网页、Markdown 和 SVG；`assets` 存放样式及搜索逻辑。`seed_content.py` 仅用于重建初始数据，日常编辑请直接修改 JSON，避免覆盖已有更新。

## GitHub Pages

仓库 Settings → Pages → Build and deployment 的 Source 选择 **GitHub Actions**。推送 `main` 后，工作流构建并部署 `dist`。所有站内链接采用相对地址，支持 `/ai-knowledge/` 项目路径。`dist` 一并保留便于直接查看和迁移。

## 许可

原创文字与 SVG 示意图： [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hans)。
构建代码和页面样式：MIT，见 [LICENSE](LICENSE)。第三方资料归原作者，遵循其各自许可。

## 第二批扩充（2026-11-04）

从20篇扩充至60篇，新增训练与对齐、多模态两专题；原有20篇入口保持不变。每篇可沿前置阅读、相关主题和上一篇/下一篇继续阅读。搜索包含正文、术语与比较表。图示按概念使用流程、分支、反馈循环、并列比较或时间阶段，窄屏可在图表容器内左右滑动。

目前是持续完善的知识库，不声称已覆盖全部AI知识。高阶数学证明、完整训练操作、厂商配置教程和实时行情不属于当前的无需编程阅读目标。
