"""Canonical, deterministic contracts for parsed security evidence.

These dataclasses are intentionally small and frozen so that facts extracted
from vendor configuration text remain auditable, stable, and safe to pass
through the rest of the compliance pipeline without accidental mutation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True, slots=True)
class Evidence:
    """Traceable source evidence for a parsed security fact.

    The combination of ``source``, ``raw_text``, and ``line_number`` must be
    sufficient to reproduce how a fact was extracted from the original input.
    """

    source: str
    raw_text: str
    line_number: Optional[int] = None


@dataclass(frozen=True, slots=True)
class SecurityFact:
    """Deterministic vendor-neutral fact emitted by a parser.

    ``fact_id`` is a stable identifier, ``rule_type`` describes the semantic
    meaning, ``value`` stores the normalized observation, and ``evidence``
    preserves the exact source line that justified the fact.
    """

    fact_id: str
    rule_type: str
    value: Any
    evidence: Evidence


__all__ = ["Evidence", "SecurityFact"]
