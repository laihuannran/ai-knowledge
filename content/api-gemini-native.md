# Gemini 原生接口：区分生成内容与交互状态

> 同时理解 Generate Content 和 Interactions，守住多 parts、函数回执、思考签名与服务端状态的边界。

专题：接入平台 · 整理于 2026-11-05

## 前置阅读

- [模型 API 地图：先分接口、模型、平台与客户端](api-protocol-map.md)
- [上下文装配：决定模型这一轮看见什么](context-assembly.md)

## 先用一个类比理解

像两种工作台账：一种每次递交材料包，另一种按交互编号连接步骤；附件和回执仍须准确归档。

类比只帮助建立直觉，不等同于完整机制。

## 一图看懂

![同时理解 Generate Content 和 Interactions，守住多 parts、函数回执、思考签名与服务端状态的边界。](../dist/diagrams/api-gemini-native.svg)

## 先辨认两代原生接口

当前 Gemini 原生能力不能只用 contents 一个字段概括。官方已经推荐新项目考虑 Interactions，同时明确 Generate Content 继续受到支持。Interactions 用 input 与步骤表示交互，并可通过 previous_interaction_id 连接服务端保存的交互；Generate Content 则以 contents、parts 和 candidates 组织请求与响应。两者属于不同接口契约，不能把一个接口的返回直接当作另一个的历史。

选择入口时，先确认现有系统依赖的是无状态生成、SDK 聊天封装，还是服务端管理的交互。文档中的推荐不会自动迁移已有应用，也不保证每个模型、地区和托管平台同时支持同一能力。先记录接口、版本、功能与状态模式，后续讨论字段才有确定含义。

## contents 里面装的是轮次和 parts

在 Generate Content 中，contents 是对话内容序列，每项 Content 通过 role 与 parts 表达来源和材料。模型一侧通常使用 model 角色，不能直接照搬 assistant；systemInstruction 是单独的系统配置概念，也不是把任意 system 消息塞进 contents。SDK 命名可能采用语言习惯的形式，审阅原始协议时应核对对应字段。

parts 可以表示文字及受到支持的图像、音频、文件引用或函数内容，具体组合受模型与模式限制。一轮内容可以有多个 parts；把它们压成单段文字会失去媒体与函数的边界。图片引用存在于历史记录，也不代表文件仍有效或访问仍获授权，应把材料可用性与消息格式分别核验。

## 完整读取 candidates 与结束原因

Generate Content 响应中的 candidates 是候选集合，每个候选可含 content.parts、finishReason 等信息。只读 candidates 第一项的第一个 text，可能漏掉同轮后续文本、函数请求或其他输出。选择某个候选作为产品回答是一项明确策略，不能借此假定未选内容不存在，更不能把不同候选的 parts 混成同一轮。

finishReason 需要结合安全反馈与返回内容解释。达到限制、正常停止与被阻断是不同状态，缺少可见文字也不必然是网络故障。应先核对候选是否存在、结构是否完整，再决定展示回答、等待工具或提示无法生成。请求成功和业务任务完成是两层判断，单凭 HTTP 成功状态不能作出后者结论。

## functionCall 与 functionResponse 配对

函数声明告诉模型可以提出哪些调用；实际执行仍由应用承担。在 Generate Content 中，模型可以通过 part 的 functionCall 提供名称和参数，应用执行后用 functionResponse 回传结构化结果，并保留相应的模型调用内容。回传格式应遵循当前接口示例，调用标识在该模式要求时也必须保留，不能只用一句自然语言结果替代。

同一轮可能出现多个函数 parts，顺序或并行执行必须结合函数依赖和权限判断。查库存与查门店时间可以独立，支付与取消订单则涉及外部状态，不能因它们在同一响应中就盲目并发。自动函数调用是特定 SDK 的执行便利，不表示远端模型拥有本地函数，也不能替代用户授权和参数校验。

## Interactions 用步骤记录过程

Interactions 的 input 可以承载用户输入及允许的结构化步骤，交互结果以 steps 描述过程。user_input、model_output、function_call、function_result 等类型说明谁提供材料、模型输出什么、请求了什么函数以及执行返回什么。不能把 function_result 改名为 Generate Content 的 functionResponse 后就宣称等价，因为交互标识、步骤关联与状态管理也需要对应。

使用 previous_interaction_id 时，应确认前一个交互已按服务要求保存且仍可引用，并保留当前轮额外输入与工具回执。服务端知道部分历史不意味着它知道企业数据库中的最新状态；变更的订单事实仍需重新提供证据。若选择无状态交互，则应按该模式要求提交完整必要步骤，不能混用有状态模式的省略假设。

还需区分读取方式：interactions.create 的返回只包含模型生成的步骤；通过 interactions.get 读取已保存资源时，才能看到包括 user_input 在内的完整交互步骤。不能把两种返回体当作同一份固定字段列表。

## SDK 聊天对象不是服务端记忆

Generate Content 的 SDK 聊天封装可以替应用收集历史并在后续调用中发送，这种方便的会话对象不能证明服务端保存了一个可以永久续接的聊天。进程重启、历史裁剪和工具往返都可能改变实际输入，因此需要检查 SDK 最终提交的内容，而不是只看产品界面还显示旧对话。

Interactions 的服务端状态连接提供另一种管理方式，也有保存策略、有效期和接口要求。两者都不能免除上下文预算与版本管理。业务上可以记录订单编号、核对时间和已授权动作，让后续轮次理解进度；这些可审查状态不是隐藏思维链，也不要求把模型的内部推理复制到企业日志。

## thought signatures 按接口保留

思考签名是模型产生的不可随意改写的协议数据，不是供人解码的推理说明。在 Generate Content 中，签名可以作为 part 的元数据出现；手工维护历史时，应依官方针对该模型和调用模式的规则原样保留关联 part、签名与顺序，不能随便合并带签名和不带签名的 parts，也不能从别轮复制签名凑数。

当前 Interactions 对思考采用独立步骤表示，签名处理与 Generate Content 不同；有状态模式可以由服务端管理，无状态模式须保留该模式要求的思考步骤及相关签名。官方 SDK 的自动处理只对相应调用路径成立，经过自定义代理后仍要验证完整性。签名不是要求公开隐藏思维链，应用也不应编造一段推理代替签名。

## 流式生成与 Live 不是同义词

streamGenerateContent 是 Generate Content 的流式生成方法，分批返回生成内容；应用仍需按候选、parts 与结束信息理解各段。它不等于 Gemini Live。Live 面向实时双向交互，有独立会话、消息与媒体约束，不能因为两者都边生成边接收，就共用同一套结束判断和重连假设。

流中某次没有 text，可能是在提供其他结构或统计，不能立即视为失败。连接关闭也不能自动证明所有业务结果已完成。验收时应分别检查正常结束、用户取消、网络中断和安全终止，保存已经确认的结果及不确定状态。对于多个片段里的统计，先核对字段是累计还是增量，不能按收到片段数量直接相加。

## Developer API 与 Vertex AI 分开核对

Gemini Developer API 与 Vertex AI 是不同接入环境。前者常见 API 密钥入口，后者通常结合 Google Cloud 项目、位置与 IAM 身份授权；具体支持的鉴权形式应以所选入口当前文档为准。模型标识、版本、区域可用性、配额和功能推出节奏也可能不同，不能拿一个环境的成功截图证明另一个已可用。

OpenAI compatibility 又是一个兼容入口，其 messages、choices 等外形有利于已有客户端迁移，但不等于原生协议的所有模式都能无损表达。思考控制、签名、工具和多模态能力需要逐项核对官方映射与限制。选择兼容层时，应写清实际使用的功能集合；不要把“改了地址可以返回文字”扩大成“所有原生能力完全支持”。

## 用双轨账本检查迁移

准备同一个查库存案例，分别记录 Generate Content 的用户 contents、模型函数 part、函数回执和最终候选，以及 Interactions 的输入、函数步骤、结果步骤和后续交互引用。比较的是业务含义是否连续，而不是字段名字是否看起来相似；同一笔工具结果应始终能追溯到正确调用。

再加入多 parts、工具失败、签名保留和中断四类情况，检查迁移后是否仍能解释完整轨迹。文档会随平台演进，本文以核对日期的官方页面为依据，特别区分继续受支持的 Generate Content 与当前推荐的 Interactions。所有例子只描述观察与验收，不发起模型请求、不接触密钥，也不以模型名称或价格代替协议判断。

## 图解：两种原生组织法

![上排两项描述 Generate Content，下排两项描述 Interactions；并列观察不表示字段可以直接互换。](../dist/diagrams/api-gemini-native-detail-1.svg)

上排两项描述 Generate Content，下排两项描述 Interactions；并列观察不表示字段可以直接互换。


## 图解：函数处理循环

![继续生成可再次请求函数，循环中的每次执行都必须有独立关联。](../dist/diagrams/api-gemini-native-detail-2.svg)

继续生成可再次请求函数，循环中的每次执行都必须有独立关联。


## 放在一起对比

| 观察对象 | 原生表示 | 验收重点 |
| --- | --- | --- |
| Generate Content | contents / parts / candidates | 保留多分片与结束原因 |
| Interactions | input / steps / previous_interaction_id | 核对状态模式与步骤关联 |
| 兼容入口 | messages / choices | 逐项验证功能映射 |

## 真实场景

同一次库存查询在 Generate Content 中保留函数 part 和回执，在 Interactions 中保留调用步骤、结果步骤与可用的交互引用。

## 常见误区

把 SDK 保存的聊天历史误认为服务端持久会话，或混用两种接口的签名位置。

## 想一想

为什么只读取第一个 text 不能证明 Gemini 原生接入正确？

<details><summary>查看解释</summary>

一个候选或交互可能含多个文本、函数和其他结构；只读首段会漏掉控制信息，无法确认回执关系和最终状态。

</details>

## 关联阅读

- [OpenAI Chat Completions：消息、候选与工具往返](api-openai-chat.md)
- [OpenAI Responses：内容项、事件与会话状态](api-openai-responses.md)
- [流式适配：从字节、事件到完整工具循环](api-stream-translation.md)

## 原始资料

- [Generate Content 参考](https://ai.google.dev/api/generate-content)
- [函数调用](https://aistudio.google.com/docs/function-calling?generate-content=true)
- [生成内容中的思考](https://ai.google.dev/gemini-api/docs/generate-content/thinking)
- [Interactions 概览](https://aistudio.google.com/docs/interactions-overview)
- [当前思考说明](https://aistudio.google.com/docs/thinking)
- [OpenAI 兼容](https://ai.google.dev/gemini-api/docs/openai)

原创讲解；图示和类比经过简化，数字示例不代表实测。工具功能以对应版本官方资料为准。
