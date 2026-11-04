# AI 知识库第二批扩充 Implementation Plan

> Use subagent-driven-development for the isolated editorial task; owner integrates and validates the site. User authorized continuous expansion and publishing on 2026-11-04.

**Goal:** 从 20 篇入门文章扩展为60 篇有来源、图解和明确边界的知识库。
**Architecture:** 保留结构化内容与标准库静态构建。扩展数据合并后统一生成；增加可选比较表、前置/关联 slug 和图示类型，数量由真实数据驱动。
**Tech Stack:** Python, JSON, SVG, HTML/CSS/JS, GitHub Pages.

- [x] Editorial task (content/expansion.json only): 32 original Chinese articles plus 8 foundational and engineering supplements on foundations, training/alignment, RAG, agents, gateway/routing, inference optimization, evals, multimodality, and selection. Each has 4-6 substantive sections, source links, example, misconception, self-check, prerequisites, four diagram nodes and diagram type. Browse official sources. No copied prose or performance promises.
- [x] Builder task (scripts/build.py, scripts/diagrams.py, assets): merge approved content preserving old URLs, group pedagogically by category, derive counts dynamically, generate branch/cycle/comparison/timeline diagrams, comparison tables, curated prerequisite and related links. Ensure Markdown has the same teaching content.
- [x] Integrity task (scripts/check.py): derive expected HTML/diagram count, validate prerequisite references, metadata counts and local links, maintain deterministic build.
- [x] Editorial review: inspect new articles for coverage, unsupported claims, confused concepts, citation relevance and beginner language; fix findings before publication.
- [x] Browser verification: search, topic filtering, glossary, related links, comparison table and diagram on mobile. Check no page-wide overflow.
- [x] Release: update README and release note with actual inventory, build and check, commit and push to main via SSH; verify GitHub Actions and production page contents.

No scheduled automation is requested. Completion means this bounded expansion is published; remaining areas are documented as future scope without claiming all AI knowledge is complete.
