from typing import Protocol

from sih26155.core.evidence.models import Evidence
from sih26155.core.facts.models import SecurityFact


class ParseResult:
    def __init__(
        self,
        facts: list[SecurityFact],
        evidence: list[Evidence],
        unknown_lines: list[str],
    ):
        self.facts = facts
        self.evidence = evidence
        self.unknown_lines = unknown_lines


class VendorParser(Protocol):

    @property
    def name(self) -> str:
        ...

    def parse(
        self,
        config: str,
        source_file: str,
    ) -> ParseResult:
        ...