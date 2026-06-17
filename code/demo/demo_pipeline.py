from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.pipeline.runner import PipelineRunner


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--threshold-bps", type=int, default=7800)
    p.add_argument("--llm-provider", choices=["mock", "ollama", "openai"], default="ollama")
    p.add_argument("--mock-chain", dest="mock_chain", action="store_true", default=True)
    p.add_argument("--real-chain", dest="mock_chain", action="store_false")
    p.add_argument("--mock-payment", dest="mock_payment", action="store_true", default=True)
    p.add_argument("--real-payment", dest="mock_payment", action="store_false")
    p.add_argument("--append-usage-log", action="store_true")
    p.add_argument("--eval-provider", choices=["mock", "ollama", "openai"], default=None)
    p.add_argument("--sources-dir", default="data/sources")
    p.add_argument("--output-dir", default="output/wiki")
    args = p.parse_args()
    result = PipelineRunner(args.sources_dir, args.output_dir, args.threshold_bps, args.llm_provider, args.mock_chain, args.mock_payment, args.append_usage_log, args.eval_provider).run()
    print(json.dumps({k: result[k] for k in ["run_id", "source_files", "chunks", "pages", "passed", "failed", "certificates_on_chain", "payments", "threshold_bps", "llm_provider_requested", "eval_provider_requested", "llm_provider_used", "fallback_message"]}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
