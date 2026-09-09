from dataclasses import dataclass, field
from typing import Any, Literal


Operator = Literal[
    "eq",
    "neq",
    "gt",
    "gte",
    "lt",
    "lte",
    "in",
    "not_in",
    "truthy",
    "falsy",
]


@dataclass(frozen=True)
class PolicyRule:
    control_id: str
    semantic_field: str
    description: str
    operator: Operator
    expected: Any
    severity: str
    evidence_required: bool = True
    remediation_required: bool = False
    frameworks: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PolicyRule":
        return cls(
            control_id=data["control_id"],
            semantic_field=data["semantic_field"],
            description=data["description"],
            operator=data["operator"],
            expected=data["expected"],
            severity=str(data["severity"]).lower(),
            evidence_required=bool(data.get("evidence_required", True)),
            remediation_required=bool(
                data.get("remediation_required", False)
            ),
            frameworks=list(data.get("frameworks", [])),
        )


@dataclass(frozen=True)
class PolicySet:
    name: str
    rules: list[PolicyRule]