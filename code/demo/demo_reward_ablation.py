from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.agents.curator import WikiCuratorAgent
from src.agents.evaluator import EvalAgent
from src.agents.payer import PayAgent
from src.pipeline.chunker import load_and_chunk_sources


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

    claim_checks = sum(len(cert["claim_checks"]) for cert in certs)
    unsupported_caught = sum(
        1 for cert in certs for finding in cert["claim_checks"] if finding["verdict"] == "UNSUPPORTED"
    )
    accepted_findings = sum(
        1 for cert in certs for finding in cert["claim_checks"] if finding["curator_decision"] == "ACCEPT"
    )
    payments = len(PayAgent(mock_payment=True).reward_accepted_findings(certs))

    rows = [
        {
            "policy": "no_reward_baseline",
            "claim_checks": claim_checks,
            "unsupported_caught": unsupported_caught,
            "accepted_findings": accepted_findings,
            "payments": 0,
            "total_mock_wlc": 0.0,
            "claim": "baseline evaluation output; no payment flow activated",
        },
        {
            "policy": "accepted_finding_rewards",
            "claim_checks": claim_checks,
            "unsupported_caught": unsupported_caught,
            "accepted_findings": accepted_findings,
            "payments": payments,
            "total_mock_wlc": round(payments * 0.01, 4),
            "claim": "same mock evaluation output; accepted-finding payment flow activated",
        },
    ]

    csv_path = evidence / f"{prefix}reward_comparison.csv"
    fieldnames = [
        "policy",
        "claim_checks",
        "unsupported_caught",
        "accepted_findings",
        "payments",
        "total_mock_wlc",
        "claim",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(8, 4))
        labels = [row["policy"] for row in rows]
        plt.bar(labels, [row["payments"] for row in rows], label="payment tx count")
        plt.ylabel("payment tx count")
        plt.title("Reward Policy Activates Accepted-Finding Payments")
        plt.xticks(rotation=10, ha="right")
        plt.tight_layout()
        plt.savefig(evidence / f"{prefix}reward_comparison.png")
    except Exception as exc:
        (evidence / f"{prefix}reward_comparison.png").write_text(f"PNG generation unavailable: {exc}", encoding="utf-8")

    print(f"wrote {csv_path} and {evidence / (prefix + 'reward_comparison.png')}")


if __name__ == "__main__":
    main()
