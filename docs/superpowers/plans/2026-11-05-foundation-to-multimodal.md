# AI 基础、训练与交互能力扩展计划

日期：2026-11-05。用户授权按已有节奏补齐五类缺口并更新 GitHub 教程。

## 范围与文件责任

- content/foundation_series.json：任务版图、泛化与泄漏、神经网络学习，3篇。
- content/reasoning_series.json：测试时计算、强化学习基础、DPO与GRPO，3篇。
- content/data_training_series.json：数据生产、合成数据、训练框架、分布式训练、模型压缩，5篇。
- content/interactive_multimodal_series.json：浏览器机制与可靠性、图像控制、视频一致性、实时语音，5篇。
- content/book.json / learning_review.json：篇章顺序、五组专题导览、前置知识。
- content/research/projects.json：补齐相关训练、浏览器与生成式工具，附官方来源和日期。
- scripts/catalog.py / edition.py：接入新增文件与入口；沿用现有页面组件。
- README.md / docs/verification.md：更新实际库存及可复核验证结果。

## 内容与验收

每篇至少8节、1700实质正文字符、3张不同概念图和1张有意义对照表。不复制段尾填充；摘要、案例和问答必须完整独特。只使用官方文档、作者论文、官方项目作为技术证据，区分来源事实与本站教学例子。避免把DPO等同PPO、推理过程等同正确性、低比特等同必然加速、界面动作等同业务成功。

1. 并行整理独立内容文件，根负责研究图谱与目录集成。
2. 逐篇审查机制、图示拓扑、比较表和引用；交叉审查事实与学习门槛。
3. 构建并运行 scripts/check.py，核对所有旧文章保留、重复段落、正文长度、全部本地链接及图片。
4. 桌面和移动端抽查新导览与代表文章，验证搜索与图表阅读。
5. 提交推送main，检查Actions成功，在线新增页面与图逐字节比对。

本轮只阅读与创作，不启动训练、购买服务或执行业务操作。完成后后续再补机器人、完整MLOps与行业专题，不能宣称穷尽AI。
