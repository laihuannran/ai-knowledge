# Plain Language Edition Implementation Plan

**Goal:** 将153篇AI教程逐篇改为零基础可理解、保持深度的中文解释。
**Architecture:** 保持源JSON与书籍顺序；新增plain_intro/takeaway；构建器统一安排讲解顺序并同步Markdown及搜索。
**Tech Stack:** Python标准库、JSON、HTML/CSS、原创SVG。

- [x] 分组重写全部153篇正文，逐篇记录实际覆盖，核对参数、训练与多模态等关键误解。
- [x] 合并通俗版唯一源JSON，保留来源、文章URL与前置顺序；审查无原段落机械残留和重复填充。
- [x] 调整HTML/Markdown为直接解释、例子在前，一句话总结在后；搜索包含新增解释。
- [x] 构建验证153篇内容、引用、图和目录；抽查手机/桌面基础与深入文章。
- [x] 更新说明与核验记录，提交推送并验证Pages发布与线上内容一致。
