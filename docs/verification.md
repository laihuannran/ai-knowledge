# 首版验证记录

日期：2026-11-04。

- Python 构建成功：20 篇文章、71 个术语、24 个 HTML 页面。
- 本地完整性检查通过：所有站内文件链接和片段有效，20 张 SVG 可解析，图片具有替代文字。
- JavaScript 通过 node --check。
- 浏览器：首页 PD 分离搜索命中 1 篇，推理设施筛选 4 篇，重置后 20 篇，空结果提示正常。
- 390px 手机视口：首页与 PD 文章无整页横向溢出；图示可在容器内左右滑动。
- 38 个官方资料链接进行了 HTTP 可达检查；26 个返回 200，11 个 Hugging Face 链接在此网络超时，1 个 Milvus 链接拒绝自动访问。未将这些网络失败认定为资料失效；核心 Hugging Face 页面另通过网页检索访问。详见 content/source-checks.json。
- GitHub Actions 首次工作流 #1 的 build 与 deploy 均成功。
- 已通过 curl 检查线上首页、地图、PD 文章、脚本和 SVG 内容。

网站：https://laihuannran.github.io/ai-knowledge/
首次部署：https://github.com/laihuannran/ai-knowledge/actions/runs/41798512953

验证边界：入门图示有意简化；未进行 GPU 压测，不声明任何性能实测收益。
