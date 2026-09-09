from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sih26155.compliance.evaluator.engine import Finding
from sih26155.core.pipeline.stages import (
    build_mvp_policy,
    detect_stage,
    evaluate_stage,
    normalize_stage,
    parse_stage,
)
from sih26155.remediation.generator import RemediationGenerator
from sih26155.remediation.loader import RemediationLoader
from sih26155.remediation.registry import RemediationRegistry


@dataclass
class AnalysisResult:
    vendor: Any
    parse_result: Any
    baseline: Any
    findings: list[Finding]
    remediations: list[Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "vendor": {
                "name": self.vendor.vendor.value,
                "confidence": self.vendor.confidence,
                "matched_signatures": list(
                    self.vendor.matched_signatures
                ),
            },
            "facts": [
                {
                    "field": fact.field,
                    "value": fact.value,
                    "confidence": fact.confidence,
                    "source": fact.source.value,
                    "evidence_id": fact.evidence_id,
                }
                for fact in self.parse_result.facts
            ],
            "evidence": [
                evidence.model_dump()
                for evidence in self.parse_result.evidence
            ],
            "baseline": self.baseline.model_dump(),
            "findings": [
                finding.to_dict()
                for finding in self.findings
            ],
            "remediations": [
                remediation.__dict__
                for remediation in self.remediations
            ],
        }


def analyze_config(
    config: str,
    source_file: str,
) -> AnalysisResult:
    detection = detect_stage(config)

    parse_result = parse_stage(
        config=config,
        source_file=source_file,
        detection=detection,
    )

    baseline = normalize_stage(
        parse_result.facts,
    )

    policy = build_mvp_policy()

    findings = evaluate_stage(
        baseline=baseline,
        policy=policy,
    )

    registry = RemediationRegistry()

    remediation_path = _remediation_path(
        vendor=detection.vendor.value,
    )

    try:
        RemediationLoader.load_file(
            path=remediation_path,
            registry=registry,
        )
    except FileNotFoundError:
        pass

    failed_control_ids = [
        finding.control_id
        for finding in findings
        if finding.status == "FAIL"
    ]

    generator = RemediationGenerator(registry)

    remediations = generator.generate_for_findings(
        vendor=detection.vendor.value,
        platform="ios",
        control_ids=failed_control_ids,
    )

    return AnalysisResult(
        vendor=detection,
        parse_result=parse_result,
        baseline=baseline,
        findings=findings,
        remediations=remediations,
    )


def _remediation_path(vendor: str) -> str:
    if vendor == "cisco":
        return "data/remediation/cisco/remediations.json"

    return f"data/remediation/{vendor}/remediations.json"