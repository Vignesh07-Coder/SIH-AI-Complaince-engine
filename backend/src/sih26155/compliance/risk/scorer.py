from dataclasses import dataclass

from ..evaluator.engine import Finding
from .severity import severity_weight


@dataclass(frozen=True)
class RiskResult:
    score: float
    rating: str
    total_findings: int
    failed_findings: int
    unknown_findings: int


def _rating(score: float) -> str:
    if score < 20:
        return "LOW"

    if score < 40:
        return "MODERATE"

    if score < 70:
        return "HIGH"

    return "CRITICAL"


def calculate_risk(
    findings: list[Finding],
) -> RiskResult:
    failed = [
        finding
        for finding in findings
        if finding.status == "FAIL"
    ]

    unknown = [
        finding
        for finding in findings
        if finding.status == "UNKNOWN"
    ]

    total_weight = sum(
        severity_weight(finding.severity)
        for finding in findings
    )

    failed_weight = sum(
        severity_weight(finding.severity)
        for finding in failed
    )

    if total_weight == 0:
        score = 0.0
    else:
        score = round(
            (failed_weight / total_weight) * 100,
            2,
        )

    return RiskResult(
        score=score,
        rating=_rating(score),
        total_findings=len(findings),
        failed_findings=len(failed),
        unknown_findings=len(unknown),
    )