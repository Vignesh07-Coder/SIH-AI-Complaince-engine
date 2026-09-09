from dataclasses import dataclass, field

from sih26155.core.evidence.models import Evidence
from sih26155.core.facts.models import SecurityFact


@dataclass
class ParserOutput:
    facts: list[SecurityFact] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    unknown_lines: list[str] = field(default_factory=list)
