from typing import Protocol

from sih26155.core.facts.models import SecurityFact


class ParseResult:
    def __init__(
        self,
        facts: list[SecurityFact],
        unknown_lines: list[str],
    ):
        self.facts = facts
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