# ai_wiki 技术栈差异整理 Implementation Plan

> **For agentic workers:** 按独立内容文件分派编写，主智能体核对并集成；不得修改其他工作者文件。

**Goal:** 对照 ai_wiki 与现有 63 个技术项目，补齐有明确职责的工具链，并发布可追溯的原创中文教程。

**Architecture:** 沿现有静态书结构增加 3 组系列，各 3 篇；另写 1 篇差异导览。项目卡合并到现有图谱，保留固定源提交与官方来源，既有 URL 不变。

**Tech Stack:** Python 3 标准库、JSON、原创 SVG、GitHub Pages。

- [x] 获取 ai_wiki 完整递归目录，固定 SHA `75529711fdc892b88cb772a727bd63bcd8ce021c`；按文件路径筛选并读取代表性条目，不执行第三方代码。
- [x] 新建 `content/wiki_retrieval_series.json`：解析、表示与向量库 3 篇；`content/research/wiki_retrieval_projects.json` 暂存 7 个项目。
- [x] 新建 `content/wiki_training_series.json`：微调工作台、DeepSpeed、评测工作台 3 篇；对应暂存 6 个项目。
- [x] 新建 `content/wiki_serving_series.json`：引擎、GPUStack、应用界面 3 篇；对应暂存 5 个项目。
- [x] 新建 `content/wiki_curation.json` 与 `docs/ai-wiki-audit.md`，记录已有覆盖、此次纳入和候选领域；不把候选说成已完成教程。
- [x] 更新 `scripts/catalog.py` 加载上述 4 个内容文件；更新 `content/book.json`、`content/learning_review.json` 接入已有篇章。
- [x] 合并 18 项到 `content/research/projects.json`，补 `scripts/edition.py` 项目章节映射与首页入口；把 ai_wiki 加入参考书架并说明许可证核验范围。
- [x] 执行 `python3 scripts/build.py` 与 `python3 scripts/check.py`，核对 153 篇文章的结构、链接、图表与目录精确覆盖，审查新正文无重复填充。
- [x] 桌面及手机抽查导览、项目搜索、长文与图表；核对来源可达性。
- [ ] 提交并推送 `HEAD:main`，确认 Pages Actions 成功及生产页面与本地成品相符，记录到 `docs/verification.md`。

不要求读者编程，不复制未核明许可的第三方图文，不把 Star 当质量评分，不额外扩建网站框架。
