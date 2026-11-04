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

## 第二批扩充验证

2026-11-04：总计60篇、10专题、219术语、60张SVG、17张比较表、64个HTML页面。新增40篇经内容规格和技术准确性两阶段审查；修正位置编码示意顺序、选型图类型，并补充熔断模式来源。原有20篇URL保留。

- 全站构建、HTML/Markdown本地链接、锚点、前置依赖无环、SVG可解析、内容字段与目录数量检查通过。
- JavaScript语法检查与Python编译通过。
- 手机390px：首页与图表页无整页横向溢出，图表在独立容器滚动。
- 浏览器搜索RRF/QLoRA/SSE均找到相应专题文章；训练与对齐筛选5篇，空结果提示通过。
- HTTP可达记录共88条：61条返回200，25条Hugging Face在执行网络超时，2条Milvus拒绝自动请求；这些状态不等同于内容核验。HF多项核心页面已通过网页工具独立访问。已替换一个确认404的Elasticsearch旧路径。
- 内容审查核对了梯度、Top-p、RRF、检索指标、预算、PD容量、A/B、Softmax与带宽例子的算术。数字均为教学假设，未进行GPU压测。

构建可重复，源码和文章独立于公司仓库。
