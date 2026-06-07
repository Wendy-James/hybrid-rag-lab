# Hybrid RAG Lab

Hybrid RAG Lab 是一个面向算法实习简历的 RAG 检索增强生成项目，重点不是调用 API，而是系统性复现和分析检索链路。

当前已实现：

- 文档加载与切分
- BM25 稀疏检索
- 哈希向量稠密检索
- Query Rewrite 查询改写
- RRF 多路召回融合
- 词法 Reranker 重排
- Recall@K、MRR@K、nDCG@K 评估

## 快速运行

```bash
python -m hybrid_rag_lab.cli search --query "How does reranking improve RAG retrieval?"
python -m hybrid_rag_lab.cli evaluate --k 3
PYTHONPATH=src python scripts/run_experiment.py
```

## 当前实验结果

实验结果已保存到 `experiments/baseline/metrics.csv` 和 `experiments/baseline/metrics.json`。

| 模式 | Recall@3 | MRR@3 | nDCG@3 |
|---|---:|---:|---:|
| BM25 | 0.9000 | 1.0000 | 0.9226 |
| 稠密检索基线 | 0.9000 | 1.0000 | 0.9226 |
| Hybrid RRF | 0.9000 | 1.0000 | 0.9226 |
| Hybrid RRF + Reranker | 1.0000 | 1.0000 | 1.0000 |

## 项目亮点

- 直接实现 RAG 检索层，而不是简单调用大模型 API。
- 在同一评估脚本下对比 BM25、稠密检索基线、Hybrid RRF 和 Reranker。
- 使用 Recall@K、MRR@K、nDCG@K 量化检索质量。
- 包含架构、算法、实验和面试讲解文档。

## 优化方案

1. 将当前稠密检索基线替换为 sentence-transformer embedding。
2. 增加 FAISS FlatIP、IVF、HNSW 等索引对比。
3. 增加 Cross-Encoder Reranker 实验。
4. 扩展领域文档和更难的查询评估集。
5. 在检索质量稳定后再加入答案生成模块。

## 面试价值

这个项目可以深入讲解：

- 为什么 RAG 需要多路召回
- BM25 和向量检索的优缺点
- RRF 融合的设计思路
- Reranker 为什么能提升排序质量
- Recall@K、MRR、nDCG 的区别
- 如何从 Demo 走向可评估、可优化的工程系统
