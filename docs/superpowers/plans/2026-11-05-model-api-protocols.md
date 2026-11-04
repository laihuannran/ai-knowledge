# 模型 API 契约与协议兼容系列

用户要求整理 Chat Completions、Responses、Messages、Gemini、Bedrock、Kiro 等主流接入形态。以当前官方资料核验，避免把模型名称、产品、接口族与标准协议混为一谈。

## 内容责任
- openai_api_series.json：OpenAI Chat Completions / Responses，两篇。
- claude_gemini_api_series.json：Anthropic Messages / Gemini 原生接口，两篇。
- cloud_client_api_series.json：Bedrock 接口族 / Kiro 产品与ACP、MCP、模型接口边界，两篇。
- api_adapter_series.json：API地图、流式与工具适配、兼容性验收，三篇，由根编写。
- api_protocols.json：可查阅矩阵与官方来源；api.html 为全站独立对照入口。

每篇8节、1800以上实质正文字符、三张独特概念图、一张有意义对照表；只读资料，不调用真实模型、不读取凭据、不抓私有流量、不使用社区逆向接口作官方事实。OpenAI Docs使用官方域名搜索并实际打开；其他提供商亦只用官方技术来源。标明2026-11-05核验日期，参数支持须按模型、端点与版本判断。

## 核心验收
1. SDK helper不当作REST字段；item/content block/part/choice分别说明。
2. 请求ID、工具调用ID、会话ID与幂等语义不混用，模型建议工具调用不等于已执行。
3. SSE与AWS EventStream不混用；chunk不等于完整JSON；流结束、文本结束、工具参数结束、业务完成分开。
4. 兼容适配明确无损、条件支持、损失和不支持；不静默丢签名、工具ID、多模态或终态。
5. Bedrock的Runtime/Mantle及Converse/Invoke/OpenAI兼容路径按当前官方矩阵核验；Kiro ACP是编辑器与Agent契约，不冒充公开模型REST标准。
6. 接入新书籍分篇、学习路线、全文搜索与协议矩阵；添加api.html后更新页面库存验证。
7. 完整构建/本地链接/前置依赖/矩阵引用校验；桌面手机与筛选、流图抽查；推送、检查Actions、线上文件比对。
