from pathlib import Path

from sih26155.compliance.evaluator.engine import ComplianceEvaluator
from sih26155.compliance.policy.models import PolicyRule, PolicySet
from sih26155.core.facts.builder import build_security_baseline
from sih26155.ingestion.detection.vendor_detector import detect_vendor
from sih26155.core.schema.enums import Vendor
from sih26155.parsers.cisco.ios import CiscoIOSParser


def test_cisco_sbm_to_compliance():
    config_path = Path("data/configs/cisco/test.conf")
    config = config_path.read_text(encoding="utf-8")

    detection = detect_vendor(config)

    assert detection.vendor == Vendor.CISCO

    parse_result = CiscoIOSParser().parse(
        config=config,
        source_file=str(config_path),
    )

    baseline = build_security_baseline(parse_result.facts)

    policy = PolicySet(
        name="mvp-management-policy",
        rules=[
            PolicyRule(
                control_id="MGMT-SSH-001",
                semantic_field="management.ssh.version",
                description="SSH must use version 2.",
                operator="eq",
                expected=2,
                severity="high",
            ),
            PolicyRule(
                control_id="MGMT-TELNET-001",
                semantic_field="management.telnet.enabled",
                description="Telnet management must be disabled.",
                operator="eq",
                expected=False,
                severity="high",
            ),
            PolicyRule(
                control_id="MGMT-HTTP-001",
                semantic_field="management.http.enabled",
                description="HTTP management must be disabled.",
                operator="eq",
                expected=False,
                severity="high",
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

    findings = ComplianceEvaluator().evaluate(
        sbm=baseline,
        policy=policy,
    )

    by_control = {
        finding.control_id: finding
        for finding in findings
    }

    assert by_control["MGMT-SSH-001"].status == "PASS"
    assert by_control["MGMT-TELNET-001"].status == "PASS"
    assert by_control["MGMT-HTTP-001"].status == "FAIL"

    assert by_control["AUTH-LOGIN-001"].status == "UNKNOWN"
    assert by_control["LOG-001"].status == "UNKNOWN"