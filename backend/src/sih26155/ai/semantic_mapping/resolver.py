from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sih26155.ai.retrieval.retriever import Retriever


@dataclass(frozen=True)
class SemanticMappingResult:
    """
    Candidate semantic interpretation of an unknown configuration command.
    """

    field: str
    value: Any
    confidence: float
    reason: str


class DefaultSemanticResolver:
    """
    Deterministic baseline semantic resolver.

    It retrieves known mappings and converts them into semantic candidates.

    A future LLM/embedding-based resolver can implement the same boundary
    without changing callers.
    """

    def __init__(self, retriever: Retriever) -> None:
        self.retriever = retriever

    def resolve(
        self,
        unknown_text: str,
        context: str | None = None,
    ) -> list[SemanticMappingResult]:
        candidates = self.retriever.retrieve(
            unknown_text=unknown_text,
            context=context,
        )

        results: list[SemanticMappingResult] = []

        for candidate in candidates:
            field = candidate.get("field")

            if not field:
                continue

            value = candidate.get("value")
            score = float(candidate.get("_score", 0.0))

            confidence = min(max(score, 0.0), 1.0)

            source_text = candidate.get(
                "source_text",
                "known mapping",
            )

            reason = (
                f"Retrieved mapping similar to known command "
                f"'{source_text}'."
            )

            results.append(
                SemanticMappingResult(
                    field=field,
                    value=value,
                    confidence=confidence,
                    reason=reason,
                )
            )

        if results:
            return results

        return self._fallback_resolve(
            unknown_text=unknown_text,
            context=context,
        )

    @staticmethod
    def _fallback_resolve(
        unknown_text: str,
        context: str | None,
    ) -> list[SemanticMappingResult]:
        """
        Conservative fallback for commands that have not yet been learned.

        This does not claim high confidence. It provides a candidate that
        can later enter the human approval/learning workflow.
        """

        text = unknown_text.lower()

        if "ssh" in text and (
            "version" in text
            or "protocol" in text
            or "v2" in text
        ):
            version = 2 if "v2" in text or "version 2" in text else None

            if version is not None:
                return [
                    SemanticMappingResult(
                        field="management.ssh.version",
                        value=version,
                        confidence=0.35,
                        reason=(
                            "Fallback semantic heuristic detected "
                            "an SSH protocol version command."
                        ),
                    )
                ]

        return [
            SemanticMappingResult(
                field="unknown",
                value=unknown_text,
                confidence=0.0,
                reason=(
                    "No known semantic mapping was found; "
                    "human review is required."
                ),
            )
        ]
