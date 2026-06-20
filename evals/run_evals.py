"""Tiny eval runner for the local deterministic agent."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agent.planner import RetailOpsAgent  # noqa: E402


def main() -> int:
    cases = json.loads((ROOT / "evals" / "eval_cases.json").read_text(encoding="utf-8"))
    agent = RetailOpsAgent.from_default_data()
    results = []

    for case in cases:
        response = agent.answer(case["question"])
        passed = response["decision"] == case["expected_decision"]
        results.append(
            {
                "name": case["name"],
                "use_case": case.get("use_case", "uncategorized"),
                "passed": passed,
                "expected": case["expected_decision"],
                "actual": response["decision"],
                "source_count": len(response.get("sources", [])),
            }
        )

    report_dir = ROOT / "evals" / "reports"
    report_dir.mkdir(exist_ok=True)
    (report_dir / "latest.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    passed_count = sum(1 for result in results if result["passed"])
    print(f"evals: {passed_count}/{len(results)} passed")
    by_use_case = defaultdict(lambda: {"passed": 0, "total": 0})
    for result in results:
        bucket = by_use_case[result["use_case"]]
        bucket["total"] += 1
        bucket["passed"] += int(result["passed"])
    for use_case, summary in sorted(by_use_case.items()):
        print(f"{use_case}: {summary['passed']}/{summary['total']} passed")
    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(
            f"{status} {result['name']}: "
            f"expected={result['expected']} actual={result['actual']} sources={result['source_count']}"
        )
    return 0 if passed_count == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
