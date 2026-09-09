from __future__ import annotations

from typing import Any

from sih26155.compliance.evaluator.engine import (
    ComplianceEvaluator,
    Finding,
)
from sih26155.compliance.policy.models import PolicyRule, PolicySet
from sih26155.core.facts.builder import build_security_baseline
from sih26155.core.schema.models import SecurityBaseline
from sih26155.ingestion.detection.vendor_detector import (
    VendorDetectionResult,
    detect_vendor,
)
from sih26155.parsers.cisco.ios import CiscoIOSParser


def detect_stage(config: str) -> VendorDetectionResult:
    return detect_vendor(config)


def parse_stage(
    config: str,
    source_file: str,
    detection: VendorDetectionResult,
):
    if detection.vendor.value == "cisco":
        return CiscoIOSParser().parse(
            config=config,
            source_file=source_file,
        )

    raise ValueError(
        f"No parser is registered for vendor: {detection.vendor.value}"
    )


def normalize_stage(
    facts: list[Any],
) -> SecurityBaseline:
    return build_security_baseline(facts)


def evaluate_stage(
    baseline: SecurityBaseline,
    policy: PolicySet,
) -> list[Finding]:
    evaluator = ComplianceEvaluator()

    return evaluator.evaluate(
        sbm=baseline,
        policy=policy,
    )


def build_mvp_policy() -> PolicySet:
    return PolicySet(
        name="mvp-management-policy",
        rules=[
            PolicyRule(
                control_id="MGMT-SSH-001",
                semantic_field="management.ssh.version",
                description="SSH must use version 2.",
                operator="eq",
                expected=2,
                severity="high",
                remediation_required=True,
            ),
            PolicyRule(
                control_id="MGMT-TELNET-001",
                semantic_field="management.telnet.enabled",
                description="Telnet management must be disabled.",
                operator="eq",
                expected=False,
                severity="high",
                remediation_required=True,
            ),
            PolicyRule(
                control_id="MGMT-HTTP-001",
                semantic_field="management.http.enabled",
                description="HTTP management must be disabled.",
                operator="eq",
                expected=False,
                severity="high",
                remediation_required=True,
            ),
            PolicyRule(
                control_id="AUTH-LOGIN-001",
                semantic_field="authentication.login_protection.enabled",
                description="Login protection must be enabled.",
                operator="eq",
                expected=True,
                severity="medium",
            ),
            PolicyRule(
                control_id="LOG-001",
                semantic_field="logging.enabled",
                description="Security logging must be enabled.",
                operator="eq",
                expected=True,
                severity="medium",
            ),
        ],
    )