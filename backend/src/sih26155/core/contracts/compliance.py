from typing import Protocol

from sih26155.core.schema.models import SecurityBaseline


class Finding:
    def __init__(
        self,
        control_id: str,
        status: str,
        severity: str,
        description: str,
        expected: object,
        observed: object,
        evidence: list,
    ):
        self.control_id = control_id
        self.status = status
        self.severity = severity
        self.description = description
        self.expected = expected
        self.observed = observed
        self.evidence = evidence


class ComplianceEvaluator(Protocol):

    def evaluate(
        self,
        baseline: SecurityBaseline,
        policy_pack: str,
    ) -> list[Finding]:
        ...