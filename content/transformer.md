# Transformer、Attention 和 MoE：不看公式也能理解

> Attention 让当前位置利用相关上下文；MoE 让部分计算由选中的专家模块完成。

专题：模型能力 · 整理于 2026-11-04

## 先用一个类比理解

读“苹果发布了新手机”时，你会根据“发布”和“手机”判断苹果是公司。Attention 的类比是按当前需要给上下文信息分配不同权重，但它不是人类注意力的完整模拟。

## 一图看懂

![Attention 让当前位置利用相关上下文；MoE 让部分计算由选中的专家模块完成。](../dist/diagrams/transformer.svg)

## Transformer 是模型架构

它规定一组计算模块如何组织。位置相关信息帮助模型区分顺序，Attention 处理上下文关系，前馈网络对表示进行变换。很多语言模型沿用这类架构，但 AI 模型不限于这一种。

## MoE 的专家不是一群聊天机器人

Mixture of Experts 通常指模型内部的专家网络。路由模块为 Token 选择部分专家计算。总参数和每个 Token 激活的参数不同；激活较少不意味着所有权重都不需要存储。

## 架构名不能直接当成绩单

质量还取决于数据、训练和任务。MoE 会带来专家负载与通信问题。不要只用参数数量比较质量或推断实际延迟，要看匹配场景的测量。

## 真实场景

两款模型都写着“MoE”，一个擅长代码，一个更适合多语言问答，并不矛盾。架构只是能力来源之一。

## 常见误区

MoE 的内部专家路由，与网关把请求发给不同大模型，是两个层级的概念。

## 想一想

MoE 的专家能直接理解成多个独立 Agent 吗？

<details><summary>查看解释</summary>

不能。前者是神经网络内部模块，后者是应用层的执行角色。

</details>

## 原始资料

- [Hugging Face · Transformers 模型说明](https://huggingface.co/docs/transformers/model_doc/mixtral)
- [Hugging Face · Transformer 如何工作](https://huggingface.co/learn/llm-course/chapter1/4)

原创入门讲解；类比和示意图经过简化。工具功能以对应版本官方文档为准。
