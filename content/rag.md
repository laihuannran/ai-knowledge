# RAG：让模型先查资料，再组织答案

> RAG 是检索增强生成，把相关外部材料送给模型作为回答依据。

专题：AI 应用 · 整理于 2026-11-04

## 前置阅读

- [Token、上下文和幻觉：为什么它会忘，也会编？](tokens-context.md)

## 先用一个类比理解

像开卷考试：先找到相关书页，再根据书页回答。找到的页不对、书过期、看错内容，都可能导致答案出错。

类比只帮助建立直觉，不等同于完整机制。

## 一图看懂

![RAG 是检索增强生成，把相关外部材料送给模型作为回答依据。](../dist/diagrams/rag.svg)

## 离线准备与在线回答

资料准备时，系统解析文件、切分片段并建立索引。用户提问后，系统检索候选资料，必要时重排序，再把选中内容放进上下文。检索和生成是不同环节，应分别观察。

## Embedding、向量库、Reranker

Embedding 把内容映射成便于比较的数值表示；向量库管理这些表示并支持相似性搜索；Reranker 对问题与候选片段做更细的相关性排序。关键词检索也很有用，混合检索可以组合两类信号。

## 权限与证据要跟着资料走

索引更新、访问权限、片段出处和删除策略都影响可信度。相似不是事实相同，检索到旧制度就可能给出旧答案。模型应该能够说资料不足，引用也必须能回到原文验证。

## 真实场景

问“今年出差住宿标准是多少”，检索命中去年的规定，即使模型忠实复述也不满足需求。这时应修复资料时效和检索，而不只是换模型。

## 常见误区

RAG 通常不修改权重；它也不是把整个数据库一次性塞进模型。

## 想一想

回答错了，为什么先检查检索结果？

<details><summary>查看解释</summary>

如果相关材料未找到或已过期，生成模型往往没有足够依据。

</details>

## 关联阅读

- [解析与切块：知识库先要读对文档](rag-parsing.md)
- [混合检索与 RRF：让关键词和语义互补](hybrid-rrf.md)
- [重排：候选找到了，为什么还要再排一次](reranking.md)
- [Recall、MRR 与 nDCG：检索到底好在哪](retrieval-metrics.md)

## 原始资料

- [LangChain · Retrieval 概念](https://docs.langchain.com/oss/python/langchain/retrieval)
- [Sentence Transformers · 检索与重排](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

原创讲解；图示和类比经过简化，数字示例不代表实测。工具功能以对应版本官方资料为准。
