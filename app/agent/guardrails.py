"""Refusal rules for the retail operations agent."""

from __future__ import annotations


REFUSAL_PATTERNS = {
    "guarantee": "I cannot guarantee future inventory availability. I can only provide a grounded assessment from current inventory, order, and capacity signals.",
    "private": "I cannot process private customer data or personally identifiable information in this public demo.",
    "medical": "This retail operations demo cannot answer medical, legal, or regulated advice questions.",
}


def refusal_for(question: str) -> str | None:
    q = question.lower()
    if any(term in q for term in ("guarantee", "promise available tomorrow", "certain tomorrow")):
        return REFUSAL_PATTERNS["guarantee"]
    if any(term in q for term in ("customer email", "phone number", "credit card", "address for customer")):
        return REFUSAL_PATTERNS["private"]
    if any(term in q for term in ("diagnose", "prescribe", "legal advice")):
        return REFUSAL_PATTERNS["medical"]
    return None

