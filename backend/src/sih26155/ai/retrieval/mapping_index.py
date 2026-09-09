from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class MappingIndex:
    """
    File-backed mapping index used by the AI semantic mapping layer.

    Vendor mappings and learned mappings are stored as JSON files.
    The index is responsible only for retrieving relevant mappings.

    It does not make compliance decisions.
    """

    def __init__(
        self,
        vendor_dir: str,
        learned_dir: str,
    ) -> None:
        self.vendor_dir = Path(vendor_dir)
        self.learned_dir = Path(learned_dir)

        self.vendor_dir.mkdir(parents=True, exist_ok=True)
        self.learned_dir.mkdir(parents=True, exist_ok=True)

    def search(
        self,
        query: str,
        *,
        vendor: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        query_tokens = self._tokenize(query)

        if not query_tokens:
            return []

        mappings = self._load_mappings(vendor)

        scored: list[tuple[float, dict[str, Any]]] = []

        for mapping in mappings:
            source_text = str(mapping.get("source_text", ""))
            candidate_tokens = self._tokenize(source_text)

            score = self._similarity(
                query_tokens,
                candidate_tokens,
            )

            if score > 0:
                scored.append((score, mapping))

        scored.sort(key=lambda item: item[0], reverse=True)

        return [
            {
                **mapping,
                "_score": score,
            }
            for score, mapping in scored[:limit]
        ]

    def _load_mappings(
        self,
        vendor: str | None,
    ) -> list[dict[str, Any]]:
        mappings: list[dict[str, Any]] = []

        for directory in (
            self.vendor_dir,
            self.learned_dir,
        ):
            if not directory.exists():
                continue

            for path in directory.glob("*.json"):
                file_vendor = self._vendor_from_filename(path)

                if (
                    vendor is not None
                    and file_vendor is not None
                    and file_vendor.lower() != vendor.lower()
                ):
                    continue

                try:
                    data = json.loads(
                        path.read_text(encoding="utf-8")
                    )
                except (OSError, json.JSONDecodeError):
                    continue

                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            mappings.append(item)

        return mappings

    @staticmethod
    def _vendor_from_filename(
        path: Path,
    ) -> str | None:
        stem = path.stem

        if "_" not in stem:
            return None

        return stem.split("_", 1)[0]

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        """
        Tokenize configuration syntax while normalizing punctuation.
        """

        return set(
            re.findall(
                r"[a-z0-9]+",
                text.lower(),
            )
        )

    @staticmethod
    def _similarity(
        query_tokens: set[str],
        candidate_tokens: set[str],
    ) -> float:
        """
        Calculate semantic-retrieval confidence from token overlap.

        Exact token overlap provides the base score.

        Configuration commands often express the same concept using
        different words, so related protocol/version indicators receive
        additional weight.
        """

        if not query_tokens or not candidate_tokens:
            return 0.0

        intersection = query_tokens & candidate_tokens

        base_score = (
            len(intersection) / len(query_tokens)
        )

        bonus = 0.0

        # Protocol/domain overlap.
        protocol_terms = {
            "ssh",
            "telnet",
            "http",
            "https",
            "snmp",
            "ftp",
        }

        if query_tokens & candidate_tokens & protocol_terms:
            bonus += 0.15

        # Version semantics.
        query_has_version = (
            "version" in query_tokens
            or any(token.startswith("v") and token[1:].isdigit()
                   for token in query_tokens)
            or any(token.isdigit() for token in query_tokens)
        )

        candidate_has_version = (
            "version" in candidate_tokens
            or any(
                token.startswith("v") and token[1:].isdigit()
                for token in candidate_tokens
            )
            or any(token.isdigit() for token in candidate_tokens)
        )

        if query_has_version and candidate_has_version:
            bonus += 0.15

        return min(base_score + bonus, 1.0)