from typing import Protocol

from sih26155.core.evidence.models import Evidence
from sih26155.core.facts.models import SecurityFact


class ParseResult:
    def __init__(
        self,
        facts: list[SecurityFact],
        evidence: list[Evidence],
        unknown_lines: list[str] | None = None,
    ):
        self.facts = facts
        self.evidence = evidence
        self.unknown_lines = unknown_lines or []


class VendorParser(Protocol):
    def parse(self, config: str, source_file: str) -> ParseResult:
        ...


Parser = VendorParser
