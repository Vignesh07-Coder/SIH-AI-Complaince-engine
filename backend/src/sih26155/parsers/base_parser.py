"""Abstract contract for deterministic vendor configuration parsers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from sih26155.core.core_contracts import SecurityFact


class BaseParser(ABC):
    """Base class for vendor-specific raw configuration parsers."""

    @property
    def name(self) -> str:
        """Return a canonical parser name derived from the class name."""

        return self.__class__.__name__.removesuffix("Parser").lower()

    @abstractmethod
    def parse(self, raw_data: str) -> List[SecurityFact]:
        """Convert raw configuration text into canonical security facts."""


__all__ = ["BaseParser"]
