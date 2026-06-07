from __future__ import annotations

import csv
import json
from pathlib import Path

from hybrid_rag_lab.data import load_corpus, load_queries
from hybrid_rag_lab.evaluate import evaluate
from hybrid_rag_lab.pipeline import HybridRAGPipeline


MODES = ["bm25", "dense", "hybrid", "hybrid_rerank"]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    output_dir = root / "experiments" / "baseline"
    output_dir.mkdir(parents=True, exist_ok=True)

    pipeline = HybridRAGPipeline(load_corpus(root / "data" / "corpus.jsonl"))
    queries = load_queries(root / "data" / "queries.jsonl")
    rows = []
    for mode in MODES:
        metrics = evaluate(pipeline, queries, mode=mode, k=3)
        rows.append(
            {
                "mode": mode,
                "recall@3": round(metrics.recall_at_k, 4),
                "mrr@3": round(metrics.mrr_at_k, 4),
                "ndcg@3": round(metrics.ndcg_at_k, 4),
            }
        )

    csv_path = output_dir / "metrics.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["mode", "recall@3", "mrr@3", "ndcg@3"])
        writer.writeheader()
        writer.writerows(rows)

    json_path = output_dir / "metrics.json"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump({"k": 3, "rows": rows}, handle, indent=2)
        handle.write("\n")

    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()

