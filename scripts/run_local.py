"""Run a local scripted demo of the retail operations agent."""

from __future__ import annotations

from pathlib import Path
import logging
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agent.planner import RetailOpsAgent  # noqa: E402


QUESTIONS = [
    "Why is SKU-1842 showing available but failing pickup orders in Store 117?",
    "Route this BOPIS order for ZIP 27701 with SLA under 2 hours.",
    "We are entering Black Friday mode. Which stores should stop accepting ship-from-store orders?",
    "Can you guarantee this item will be available tomorrow?",
    "Show the evidence behind your routing decision.",
]


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    agent = RetailOpsAgent.from_default_data()
    for question in QUESTIONS:
        response = agent.answer(question)
        print(f"\nQ: {question}")
        print(f"A: {response['answer']}")
        print(f"Decision: {response['decision']}")
        if response.get("sources"):
            print(f"Sources: {response['sources']}")


if __name__ == "__main__":
    main()
