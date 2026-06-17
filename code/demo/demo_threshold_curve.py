from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.agents.curator import WikiCuratorAgent
from src.agents.evaluator import EvalAgent
from src.pipeline.chunker import load_and_chunk_sources


THRESHOLDS = [6000, 7000, 7800, 8500, 9000]
SAMPLE_FIXTURES = [
    {"sample_id": "sample_supported_strong", "score_bps": 9200, "critical": False, "unsupported_accepted": 0},
    {"sample_id": "sample_supported_good", "score_bps": 8700, "critical": False, "unsupported_accepted": 0},
    {"sample_id": "sample_supported_borderline", "score_bps": 8100, "critical": False, "unsupported_accepted": 0},
    {"sample_id": "sample_partial_below_gate", "score_bps": 7600, "critical": False, "unsupported_accepted": 1},
    {"sample_id": "sample_weak_below_gate", "score_bps": 7200, "critical": False, "unsupported_accepted": 1},
    {"sample_id": "sample_critical_hallucination", "score_bps": 0, "critical": True, "unsupported_accepted": 3},
]


def _passes(score_bps: int, critical: bool, threshold_bps: int) -> bool:
    return score_bps >= threshold_bps and not critical


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--llm-provider", choices=["mock", "ollama", "openai"], default="ollama")
    parser.add_argument("--sources-dir", default="data/sources")
    parser.add_argument("--evidence-dir", default="evidence")
    parser.add_argument("--output-prefix", default="")
    args = parser.parse_args()

    evidence = Path(args.evidence_dir)
    evidence.mkdir(exist_ok=True)
    prefix = f"{args.output_prefix}_" if args.output_prefix else ""

    chunks = load_and_chunk_sources(args.sources_dir)
    pages = WikiCuratorAgent(llm_provider=args.llm_provider).generate_wiki_pages(chunks)
    certs = EvalAgent(threshold_bps=7800, llm_provider=args.llm_provider).evaluate_all(pages, chunks)
    real_scores = [int(cert["score_bps"]) for cert in certs]

    sample_path = evidence / f"{prefix}sample_evaluation_fixtures.csv"
    with sample_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["sample_id", "score_bps", "critical", "decision_at_7800", "unsupported_accepted"],
        )
        writer.writeheader()
        for fixture in SAMPLE_FIXTURES:
            passed = _passes(int(fixture["score_bps"]), bool(fixture["critical"]), 7800)
            writer.writerow({**fixture, "decision_at_7800": "PASS" if passed else "FAIL"})

    rows = []
    for threshold in THRESHOLDS:
        real_passed = sum(score >= threshold for score in real_scores)
        sample_passed = sum(
            _passes(int(fixture["score_bps"]), bool(fixture["critical"]), threshold)
            for fixture in SAMPLE_FIXTURES
        )
        sample_certified_unsupported = sum(
            int(fixture["unsupported_accepted"])
            for fixture in SAMPLE_FIXTURES
            if _passes(int(fixture["score_bps"]), bool(fixture["critical"]), threshold)
        )
        sample_total_unsupported = sum(int(fixture["unsupported_accepted"]) for fixture in SAMPLE_FIXTURES)
        unsupported_accepted_rate = (
            round((sample_certified_unsupported / sample_total_unsupported) * 100, 1)
            if sample_total_unsupported
            else 0.0
        )
        rows.append(
            {
                "threshold_bps": threshold,
                "large_batch_real_passed": real_passed,
                "large_batch_real_failed": len(real_scores) - real_passed,
                "sample_fixture_pages": len(SAMPLE_FIXTURES),
                "sample_certified_pages": sample_passed,
                "sample_failed_pages": len(SAMPLE_FIXTURES) - sample_passed,
                "unsupported_accepted_rate_pct": unsupported_accepted_rate,
            }
        )

    csv_path = evidence / f"{prefix}threshold_curve.csv"
    fieldnames = [
        "threshold_bps",
        "large_batch_real_passed",
        "large_batch_real_failed",
        "sample_fixture_pages",
        "sample_certified_pages",
        "sample_failed_pages",
        "unsupported_accepted_rate_pct",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    try:
        import matplotlib.pyplot as plt

        thresholds = [row["threshold_bps"] for row in rows]
        certified = [row["sample_certified_pages"] for row in rows]
        unsupported_rates = [row["unsupported_accepted_rate_pct"] for row in rows]

        fig, ax1 = plt.subplots(figsize=(7, 4))
        ax1.plot(thresholds, certified, marker="o", color="tab:blue", label="certified sample pages")
        ax1.set_xlabel("threshold_bps")
        ax1.set_ylabel("certified sample pages", color="tab:blue")
        ax1.tick_params(axis="y", labelcolor="tab:blue")

        ax2 = ax1.twinx()
        ax2.plot(thresholds, unsupported_rates, marker="s", color="tab:red", label="unsupported accepted rate")
        ax2.set_ylabel("unsupported accepted rate (%)", color="tab:red")
        ax2.tick_params(axis="y", labelcolor="tab:red")

        plt.title("Threshold vs Certification and Unsupported Acceptance")
        fig.tight_layout()
        plt.savefig(evidence / f"{prefix}threshold_curve.png")
    except Exception as exc:
        (evidence / f"{prefix}threshold_curve.png").write_text(f"PNG generation unavailable: {exc}", encoding="utf-8")

    print(f"wrote {csv_path}, {sample_path}, and {evidence / (prefix + 'threshold_curve.png')}")


if __name__ == "__main__":
    main()
