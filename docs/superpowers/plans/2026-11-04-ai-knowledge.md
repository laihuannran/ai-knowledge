# AI 图解知识库 Implementation Plan

> Inline execution in the current session, following executing-plans.

**Goal:** 交付无需编程的 AI 图解知识站及可部署到 GitHub Pages 的独立源码。
**Architecture:** Python 标准库构建静态 HTML；JSON 保存结构化文章；本地 SVG 图不依赖 CDN；浏览器 JS 搜索和分类。GitHub Actions 构建并发布 Pages。
**Tech Stack:** Python 3, HTML, CSS, JavaScript, SVG, GitHub Pages.

- [x] 资料：查阅官方文档，编写 content/articles.json 的八专题文章，核验定义、类比边界与来源。
- [x] 页面：scripts/build.py 生成 dist/index.html、dist/articles/*.html 与各页 SVG，复制 assets/style.css 与 assets/app.js。所有链接使用相对路径，支持项目站路径。
- [x] 导航：首页专题筛选、全文搜索、知识地图，文章有目录、上一课下一课、参考链接。
- [x] 发布：.github/workflows/pages.yml 配置 Python 构建及官方 Pages artifact/deploy；README.md 记录阅读和部署方式。
- [x] 验证：python3 scripts/build.py；脚本校验全部本地 href/src；node --check assets/app.js；浏览器检查首页、搜索、文章和窄屏。
- [x] Git：新建独立仓库，提交内容；通过已登录 GitHub 页面或受支持凭据创建远端并推送；若无登录权限则保留完整成果并明确阻塞点。
