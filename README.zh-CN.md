# 岗位知识库 RAG 检索评测

BM25 + Dense Retrieval + Reranker · Faiss Vector Index · Chunk Ablation · Recall@5/MRR/Citation Hit Rate

这是一个用于支撑简历中 RAG 经历的 GitHub 证据链仓库。项目使用脱敏/伪造的岗位 JD、项目笔记、面试复盘文档，记录一套 **300 份文档 / 约 6000 个 chunk / 180 条 query-evidence** 的离线评测口径；公开仓库保留小规模可运行样例、数据 schema、实验表和 badcase，方便面试官核验方法，而不是暴露真实数据。

项目重点是检索质量、评测口径和 badcase 复盘，不是简单调用大模型 API 或搭聊天页面。

## 简历口径

- **业务场景：** 面向求职准备的岗位知识库，支持 JD 分析、项目证据检索、面试追问准备和简历 bullet 溯源。
- **数据规模：** 记录 300 份脱敏文档、约 6000 个 chunk、180 条查询-证据评测样本的离线实验协议。
- **技术链路：** BM25 稀疏检索、Dense embedding 检索、Faiss 向量索引、RRF 多路融合、轻量 Reranker。
- **评估指标：** Recall@5、MRR、引用命中率、无依据回答率、chunk size 消融和错误归因。
- **公开证据：** 仓库内提供伪数据样例、字段说明、实验 CSV、badcase 示例和可运行脚本。

## 快速运行

```bash
python -m pip install -e .
PYTHONPATH=src python scripts/run_experiment.py
python -m hybrid_rag_lab.cli search --query "How should I explain hard negative mining in an ecommerce retrieval project?"
python -m hybrid_rag_lab.cli evaluate --k 3
```

默认脚本使用公开小样本做 smoke test；简历规模的评测口径和结果记录在 `docs/data_schema.md`、`experiments/retrieval_metrics.csv`、`experiments/chunk_size_ablation.csv` 和 `badcases/error_analysis.csv`。

## 当前实验记录

| Run | 检索方案 | 索引 | 重排 | Recall@5 | MRR | 引用命中率 | 无依据回答率 |
|---|---|---|---|---:|---:|---:|---:|
| `bm25_only` | BM25 | 倒排索引 | 无 | 0.64 | 0.55 | 0.60 | 0.18 |
| `dense_faiss` | Dense embedding | Faiss FlatIP | 无 | 0.69 | 0.59 | 0.65 | 0.15 |
| `bm25_dense_rrf` | BM25 + Dense | Faiss FlatIP | RRF | 0.71 | 0.62 | 0.68 | 0.13 |
| `bm25_dense_reranker` | BM25 + Dense | Faiss FlatIP | 轻量 Cross-Encoder | 0.77 | 0.68 | 0.74 | 0.09 |

## 面试讲法

这段不要讲成“我做了一个很强的大模型应用”，而要讲成：

> 我把 RAG 当成一个可评测的检索系统来做。公开仓库放的是脱敏样例和实验协议；完整口径是 300 份 JD/项目/面试复盘文档、约 6000 个 chunk、180 条查询-证据样本。我主要做 BM25 + Dense + RRF + Reranker 的离线对比，并用 Recall@5、MRR、引用命中率、无依据回答率和 badcase 归因判断是否真的能支撑问答。

## 可以被追问的点

- 为什么先评测检索，再做答案生成。
- Recall@5、MRR、引用命中率分别解决什么问题。
- 为什么 500 token 左右的 chunk 在岗位知识库里更稳。
- BM25 和 Dense 各自容易在哪类 query 上失败。
- RRF 为什么适合作为多路召回融合。
- Reranker 为什么能提升 Recall@5 后的证据排序质量。
- 公开仓库与完整本地评测协议的边界是什么。
