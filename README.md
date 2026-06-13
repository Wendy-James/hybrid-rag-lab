# Job Knowledge Base RAG Evaluation

BM25 + Dense Retrieval + Reranker · Faiss Vector Index · Chunk Ablation · Recall@5/MRR/Citation Hit Rate

This repository is the GitHub evidence-chain project for a resume-side RAG retrieval evaluation system. It uses anonymized and pseudo job-description, project-note, and interview-review documents to document a **300-doc / 6000-chunk / 180-query** evaluation protocol while keeping the public repository runnable on a small smoke-test subset.

The project focus is retrieval quality and evaluation discipline, not API wrapping or chatbot UI.

## Resume-Aligned Scope

- **Scenario:** build a job-search knowledge base for JD analysis, project evidence lookup, interview question preparation, and resume-bullet grounding.
- **Data protocol:** 300 anonymized documents, about 6000 chunks after cleaning and overlap chunking, and 180 query-evidence pairs for offline regression.
- **Retrieval stack:** BM25 sparse retrieval, dense embedding retrieval, Faiss vector index, Reciprocal Rank Fusion, and lightweight reranking.
- **Evaluation:** Recall@5, MRR, citation hit rate, unsupported-answer rate, chunk-size ablation, and error analysis.
- **Public evidence:** this repo contains pseudo/anonymized samples, schemas, experiment tables, runnable local scripts, and badcase examples.

## Why This Project

Single-route dense retrieval misses exact role names, abbreviations, and rare technical terms such as `Two-Tower`, `Faiss`, `Recall@50`, or `SKU`. Pure BM25 catches keywords but misses paraphrases such as "evidence grounding" versus "citation hit". A practical RAG project needs hybrid retrieval, reranking, and stable offline metrics before adding answer generation.

## Quick Start

```bash
python -m pip install -e .
PYTHONPATH=src python scripts/run_experiment.py
python -m hybrid_rag_lab.cli search --query "How should I explain hard negative mining in an ecommerce retrieval project?"
python -m hybrid_rag_lab.cli evaluate --k 3
```

The default command runs on a compact public subset so the repository is easy to inspect. The resume-scale protocol and results are documented in `experiments/retrieval_metrics.csv`, `experiments/chunk_size_ablation.csv`, and `docs/data_schema.md`.

## Current Evidence Tables

### Retrieval Metrics

| Run | Retriever | Index | Reranker | Recall@5 | MRR | Citation Hit | Unsupported |
|---|---|---|---|---:|---:|---:|---:|
| `bm25_only` | BM25 | inverted index | none | 0.64 | 0.55 | 0.60 | 0.18 |
| `dense_faiss` | dense embedding | Faiss FlatIP | none | 0.69 | 0.59 | 0.65 | 0.15 |
| `bm25_dense_rrf` | BM25 + dense | Faiss FlatIP | RRF | 0.71 | 0.62 | 0.68 | 0.13 |
| `bm25_dense_reranker` | BM25 + dense | Faiss FlatIP | cross-encoder-lite | 0.77 | 0.68 | 0.74 | 0.09 |

### Chunk Ablation

| Chunk Size | Overlap | Chunks | Recall@5 | MRR | Note |
|---:|---:|---:|---:|---:|---|
| 300 | 60 | 8200 | 0.73 | 0.64 | Higher recall on short facts, more noisy fragments |
| 500 | 100 | 6000 | 0.77 | 0.68 | Best quality-cost balance |
| 800 | 120 | 4100 | 0.72 | 0.61 | More complete context, but diluted retrieval target |

## Project Structure

```text
hybrid-rag-lab/
  data/
    corpus.jsonl
    queries.jsonl
    sample_corpus.jsonl
    sample_queries.jsonl
  docs/
    data_schema.md
    architecture.md
    algorithm.md
    experiments.md
    interview-notes.md
  experiments/
    retrieval_metrics.csv
    chunk_size_ablation.csv
    baseline/
      metrics.csv
      metrics.json
  badcases/
    error_analysis.csv
  scripts/
    run_experiment.py
  src/hybrid_rag_lab/
    bm25.py
    dense.py
    evaluate.py
    fusion.py
    pipeline.py
    rerank.py
    rewrite.py
```

## Interview Positioning

This is a supporting project for retrieval evaluation ability. It should be described as:

> I did not package this as a large-model training project. I used anonymized JD, project, and interview-review documents to build an offline RAG retrieval evaluation set. The main deliverables were schema, chunking rules, BM25+dense retrieval, Faiss indexing notes, Recall@5/MRR/citation-hit metrics, chunk-size ablation, and badcase analysis.

## What To Discuss In Interviews

- Why Recall@K and citation hit rate matter before answer generation.
- Why chunk size around 500 tokens worked better than 300 or 800 in this domain.
- How BM25 and dense retrieval fail on different query types.
- Why RRF is used before reranking.
- Why unsupported-answer rate is tracked instead of only reporting retrieval recall.
- What the public repo contains versus what the full local evaluation protocol contains.

## Resume Summary

Built a job-knowledge RAG retrieval evaluation project using BM25, dense retrieval, Faiss-style vector indexing, RRF fusion, and lightweight reranking. Documented a 300-doc / 6000-chunk / 180-query protocol and improved Recall@5 from 0.71 to 0.77 with reranking while tracking MRR, citation hit rate, and unsupported-answer rate.
