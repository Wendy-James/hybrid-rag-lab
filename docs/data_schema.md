# Data Schema

This repository exposes anonymized and pseudo samples only. The resume-scale experiment protocol is documented so the retrieval setup can be explained and audited without publishing private job notes, interview notes, or original resume drafts.

## Corpus Protocol

| Field | Type | Example | Notes |
|---|---|---|---|
| `doc_id` | string | `project_rag_001` | Stable document id before chunking. |
| `chunk_id` | string | `project_rag_001_c004` | Unique chunk id used for retrieval labels. |
| `source_type` | enum | `job_description` | One of `job_description`, `project_note`, `interview_review`, `resume_note`. |
| `title` | string | `Job Knowledge Base RAG Evaluation` | Desensitized title. |
| `section` | string | `chunk_ablation` | Logical section after parsing. |
| `text` | string | chunk text | Cleaned and normalized chunk body. |
| `tokens` | integer | `58` | Approximate token count after cleaning. |
| `created_at` | date | `2026-06-07` | Used for version tracking, not model training. |
| `tags` | list | `["rag","retrieval"]` | Business or algorithm tags for analysis. |

Full local protocol:

- Documents: 300 anonymized JD, project-note, and interview-review documents.
- Chunking: around 6000 chunks after removing duplicate boilerplate and contact information.
- Chunk size candidates: 300/500/800 with overlaps 60/100/120.
- Final working setting: chunk size 500, overlap 100.
- Split: evaluation queries are manually held out and not used for chunk construction or reranker rule tuning.

## Query Protocol

| Field | Type | Example | Notes |
|---|---|---|---|
| `query_id` | string | `q_rag_002` | Stable query id. |
| `query` | string | user question | Interview-style or evidence-lookup query. |
| `intent` | enum | `ablation_reasoning` | Query category for badcase analysis. |
| `positive_chunk_ids` | list | `["project_rag_001_c004"]` | Evidence chunks accepted as correct. |
| `answer_hint` | string | short reference | Used only for manual checking. |
| `difficulty` | enum | `easy`, `medium`, `hard` | Difficulty bucket. |
| `tags` | list | `["chunking","ablation"]` | Topic tags. |

Full local protocol:

- Queries: 180 query-evidence pairs.
- Query categories: JD requirement lookup, project evidence lookup, metric definition, ablation reasoning, interview follow-up, and refusal/insufficient-evidence cases.
- Labeling rule: a query is counted as recalled when at least one accepted evidence chunk appears in top K.
- Citation hit rule: an answer is counted as citation-hit only when the cited chunk supports the answer claim.

## Metric Definitions

- `Recall@5`: proportion of queries where any accepted evidence chunk appears in the top 5 retrieved chunks.
- `MRR`: average reciprocal rank of the first accepted evidence chunk.
- `citation_hit_rate`: proportion of generated or drafted answers whose cited evidence supports the answer.
- `unsupported_answer_rate`: proportion of queries where the system still produces a confident answer without sufficient retrieved evidence.
- `nDCG@K`: optional graded relevance metric used in the runnable local baseline.

## Evidence Boundary

Do not describe this repository as a production system or as using company internal data. The correct interview wording is:

> The public repo contains anonymized samples and experiment tables. The point is to show the retrieval evaluation method, schema, metrics, and badcase discipline. I did not claim online deployment or private-data ownership.
