```python
from dataclasses import asdict, dataclass
from typing import Any, Literal

from ..policy.models import PolicyRule, PolicySet
from .evidence import MISSING, get_evidence, get_semantic_value
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
    evidence: list[Any]
    remediation_required: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ComplianceEvaluator:
    """
    Evaluates normalized SBM values against policy rules.

    Important:
    This class evaluates semantic values only.
    It does not parse vendor syntax.
    It does not execute remediation commands.
    It does not use AI to make compliance decisions.

    Remediation is identified from the policy rule and can be
    handled separately by the remediation layer.
    """

    def evaluate_rule(
        self,
        sbm: Any,
        rule: PolicyRule,
    ) -> Finding:
        observed = get_semantic_value(
            sbm,
            rule.semantic_field,
        )

        evidence = get_evidence(
            sbm,
            rule.semantic_field,
        )

        if observed is MISSING:
            return Finding(
                control_id=rule.control_id,
                status="UNKNOWN",
                severity=rule.severity,
                description=rule.description,
                expected=rule.expected,
                observed=None,
                evidence=evidence,
                remediation_required=False,
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
                evidence=evidence,
                remediation_required=False,
            )

        return Finding(
            control_id=rule.control_id,
            status="PASS" if passed else "FAIL",
            severity=rule.severity,
            description=rule.description,
            expected=rule.expected,
            observed=observed,
            evidence=evidence,
            remediation_required=(
                rule.remediation_required and not passed
            ),
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
```
