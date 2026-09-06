from typing import Protocol

from sih26155.core.contracts.parser import ParseResult


class ConfigurationParser(Protocol):
    """
    Interface implemented by vendor-specific configuration parsers.

    Vendor parsers convert raw configuration text into canonical
    security facts while preserving unknown configuration lines.
    """

    @property
    def name(self) -> str:
        """Return the parser's canonical name."""
        ...

    def parse(
        self,
        config: str,
        source_file: str,
    ) -> ParseResult:
        """
        Parse configuration text into canonical security facts.

        The parser must:
        - produce SecurityFact objects for recognized semantics
        - preserve source evidence
        - retain unknown lines for later AI-assisted processing
        - never perform compliance evaluation
        - never construct the final SecurityBaseline directly
        """
        ...
