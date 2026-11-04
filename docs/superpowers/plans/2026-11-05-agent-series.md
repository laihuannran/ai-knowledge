# Agent 系列补齐 Implementation Plan

**Goal:** 对照用户11张截图，补齐独立MCP、Skills、GraphRAG/Agentic RAG、Harness/上下文和企业Agent深入系列，保留书籍结构与原链接并发布。
**Architecture:** 原创长章节存于独立JSON，追加现有书籍篇章；学习对照数据说明哪些已有、哪些补深及截图中的简化边界。截图仅作为私人选题参考，不上传原图或水印个人信息。
**Tech Stack:** 现有Python/JSON/HTML/SVG构建和GitHub Pages。

- [x] 内容A content/protocol_series.json：MCP会话、工具契约、授权治理；Skills加载、组合、验收6篇。
- [x] 内容B content/retrieval_series.json：GraphRAG建图与查询、Agentic RAG、深度搜索、RAG排错、记忆生命周期6篇。
- [x] 内容C content/agent_series.json：Harness运行时、上下文工程、设计模式、意图规划、安全边界、企业案例6篇。
- [x] 对照 content/learning_review.json：提取截图主题与正确边界，对应现有或新增章节；明确七层图为教学分法而非统一标准，不复制原图。
- [x] 结构：追加各系列至现有book.json，新增guide.html进阶路线页连接主题、误区与系列，所有旧slug保留。
- [x] 调研：官方文档/原论文/GitHub核验机制，按许可原创整合，GraphRAG及记忆/Skills相关项目补入技术栈；Star无法取得则明确未获取。
- [x] 审稿：独立规格/事实审查、纠正分支图与概念层次；验证例子与失败边界。
- [ ] 验证发布：构建、目录覆盖/链接/图表/前置无环、JS和浏览器搜索与手机；提交推送并确认线上成功。
