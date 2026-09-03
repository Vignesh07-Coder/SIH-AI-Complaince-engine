from typing import Any, Protocol


class CandidateMapping:
    def __init__(
        self,
        field: str,
        value: Any,
        confidence: float,
        reason: str,
    ):
        self.field = field
        self.value = value
        self.confidence = confidence
        self.reason = reason


class SemanticResolver(Protocol):

    def resolve(
        self,
        unknown_text: str,
        context: str,
    ) -> list[CandidateMapping]:
        ...