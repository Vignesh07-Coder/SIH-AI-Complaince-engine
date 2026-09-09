from dataclasses import asdict, dataclass
from typing import Any, Literal

from ..policy.models import PolicyRule, PolicySet
from .evidence import MISSING, get_semantic_value
from .operators import evaluate_operator


FindingStatus = Literal["PASS", "FAIL", "UNKNOWN"]


@dataclass
class Finding:
    control_id: str
    status: FindingStatus
    severity: str
    description: str
    expected: Any
    observed: Any

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ComplianceEvaluator:

    def evaluate_rule(
        self,
        sbm: Any,
        rule: PolicyRule,
    ) -> Finding:

        observed = get_semantic_value(
            sbm,
            rule.semantic_field,
        )

        if observed is MISSING or observed is None:
            return Finding(
                control_id=rule.control_id,
                status="UNKNOWN",
                severity=rule.severity,
                description=rule.description,
                expected=rule.expected,
                observed=None,
            )

        try:
            passed = evaluate_operator(
                observed=observed,
                operator=rule.operator,
                expected=rule.expected,
            )
        except (TypeError, ValueError):
            return Finding(
                control_id=rule.control_id,
                status="UNKNOWN",
                severity=rule.severity,
                description=rule.description,
                expected=rule.expected,
                observed=observed,
            )

        return Finding(
            control_id=rule.control_id,
            status="PASS" if passed else "FAIL",
            severity=rule.severity,
            description=rule.description,
            expected=rule.expected,
            observed=observed,
        )

    def evaluate(
        self,
        sbm: Any,
        policy: PolicySet,
    ) -> list[Finding]:

        return [
            self.evaluate_rule(sbm, rule)
            for rule in policy.rules
        ]