from typing import Any
from pydantic import BaseModel

from sih26155.core.schema.enums import ConfidenceSource


class SecurityFact(BaseModel):
    field: str
    value: Any

    confidence: float = 1.0
    source: ConfidenceSource = ConfidenceSource.DETERMINISTIC

    evidence_id: str | None = None