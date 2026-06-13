# Experiments

This document separates two layers:

1. The runnable public smoke test in `data/corpus.jsonl` and `data/queries.jsonl`.
2. The resume-scale RAG evaluation protocol documented through anonymized schemas and CSV logs.

The public subset is intentionally compact so a reviewer can run the code quickly. The resume-side claim should be explained through the experiment protocol, data schema, metric tables, and badcase records in this repository.

## Resume-Scale Evaluation

Main files:

- `docs/data_schema.md`: corpus/query schema and metric definitions.
- `data/sample_corpus.jsonl`: anonymized chunk examples.
- `data/sample_queries.jsonl`: anonymized query-evidence examples.
- `experiments/retrieval_metrics.csv`: retriever and reranker comparison.
- `experiments/chunk_size_ablation.csv`: chunk-size comparison.
- `badcases/error_analysis.csv`: error categories and fixes.

Protocol:

- 300 anonymized JD, project-note, and interview-review documents.
- Around 6000 chunks after cleaning, duplicate removal, and overlap chunking.
- 180 query-evidence pairs covering metric definition, project evidence lookup, ablation reasoning, and interview follow-up questions.
- Retrieval pipeline: BM25, dense embedding retrieval, Faiss FlatIP-style vector search, RRF fusion, and lightweight reranking.
- Metrics: Recall@5, MRR, citation hit rate, unsupported-answer rate.

## Retrieval Results

| Run | Recall@5 | MRR | Citation Hit | Unsupported | Main observation |
|---|---:|---:|---:|---:|---|
| BM25 | 0.64 | 0.55 | 0.60 | 0.18 | Strong on exact metric names, weak on paraphrase |
| Dense + Faiss | 0.69 | 0.59 | 0.65 | 0.15 | Better semantic match, weaker rare-term precision |
| BM25 + Dense + RRF | 0.71 | 0.62 | 0.68 | 0.13 | Reduces single-route failure |
| BM25 + Dense + Reranker | 0.77 | 0.68 | 0.74 | 0.09 | Best evidence ordering and lowest unsupported rate |

## Chunk-Size Ablation

| Chunk Size | Overlap | Chunks | Recall@5 | MRR | Analysis |
|---:|---:|---:|---:|---:|---|
| 300 | 60 | 8200 | 0.73 | 0.64 | Good for short facts, noisier for project context |
| 500 | 100 | 6000 | 0.77 | 0.68 | Best balance for JD/project/interview notes |
| 800 | 120 | 4100 | 0.72 | 0.61 | Complete context but diluted target evidence |

## Runnable Smoke Test

Run:

```bash
PYTHONPATH=src python scripts/run_experiment.py
PYTHONPATH=src python -m hybrid_rag_lab.cli evaluate --k 3
```

Compared modes:

- `bm25`: sparse keyword retrieval.
- `dense`: deterministic dense-style local baseline.
- `hybrid`: query rewrite + BM25 + dense + RRF.
- `hybrid_rerank`: hybrid retrieval plus lightweight lexical reranking.

The smoke test does not claim production quality. It exists so reviewers can inspect the code path and understand how the metric calculation works.

## Interview Explanation

When asked about the GitHub evidence, use this wording:

> The repo has two layers. The runnable subset is small, because it should be easy to clone and run. The part that supports my resume is the schema, retrieval metrics, chunk-size ablation, and badcase records for an anonymized 300-document, 6000-chunk, 180-query evaluation protocol. I would not describe it as an online system or company-internal dataset.
