# Book Edition Implementation Plan

**Goal:** 发布有深度长文、书籍目录和经调研技术栈的AI教程。
**Architecture:** 现有标准库静态构建扩展结构化数据。内容、研究和导航分别维护，发布时统一校验。
**Tech Stack:** Python/JSON/HTML/CSS/JS/SVG/GitHub Pages。

- [x] 技术栈长文：content/stack_chapters.json，12篇，命名主题及架构、边界、场景、比较、官方资料。
- [x] 核心深入长文：content/deep_chapters.json，14篇，每篇至少1400正文字符（含标点与英文，非纯汉字计数），RAG/Agent/推理/评测/模型训练的完整案例和机制；每篇2个附加图或表。
- [x] 调研：content/research/projects.json 与 resources.json，至少30个按职责分类的真实项目及至少8项优质课程；记录来源与许可、star证据或明确未知。
- [x] 书籍结构：content/book.json 定义篇章系列与阅读顺序，覆盖全部文章，各章标记深度。首页变为封面和总目录入口，新增 stack.html/resources.html/library.html。
- [x] 构建：加载新增内容，支持长文分段和额外图、技术栈比较页、资料页、深度标记、每篇所属篇章与系列导航，保留原链接。
- [x] 验证：全站链接及SVG、数量与目录覆盖、项目与来源数据、长文实际深度；浏览器检查桌面/手机目录、搜索、图表。
- [ ] 两阶段审稿、修正发现问题，构建可重复；提交推送，检查Actions和线上新增内容。
