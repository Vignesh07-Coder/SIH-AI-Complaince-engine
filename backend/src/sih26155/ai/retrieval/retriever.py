from __future__ import annotations

from typing import Any

from sih26155.ai.retrieval.mapping_index import MappingIndex


class Retriever:
    """
    Retrieval boundary for semantic mapping.

    The Retriever knows how to ask the MappingIndex for relevant
    mappings. It does not interpret compliance policy.
    """

    def __init__(self, index: MappingIndex) -> None:
        self.index = index

    def retrieve(
        self,
        unknown_text: str,
        context: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        return self.index.search(
            unknown_text,
            vendor=context,
            limit=limit,
        )
