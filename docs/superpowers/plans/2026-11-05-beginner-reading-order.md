# Beginner Reading Order Implementation Plan

**Goal:** 重排目录与阅读入口，让零基础读者有连贯的浅入深路径。
**Architecture:** content/book.json 保存全书顺序、阶段与入门路线，edition.py 统一渲染，build.py 接入文章导航，check.py 验证依赖和顺序。
**Tech Stack:** Python 标准库、JSON、HTML/CSS；不增加依赖。

- [x] 重排14篇内61章及153篇文章；按实际机制修订少量前置，保留全部旧锚点。
- [x] 在首页、目录和专题页展示统一入门路线，在主线文章显示连续阅读导航。
- [x] 调整专题及其内部课次，补充自动验证前置、路线顺序与渲染入口。
- [x] 构建、检查、浏览器桌面/手机核验；更新README与验证记录。
- [ ] 提交推送、确认Pages发布，线上文件比对并记录结果。
