from sih26155.compliance.evaluator.engine import Finding
from sih26155.remediation.generator import RemediationGenerator
from sih26155.remediation.models import Remediation
from sih26155.remediation.registry import RemediationRegistry


def test_failed_finding_generates_validated_remediation():
    finding = Finding(
        control_id="MGMT-HTTP-001",
        status="FAIL",
        severity="high",
        description="HTTP management must be disabled.",
        expected=False,
        observed=True,
    )

    registry = RemediationRegistry()

    registry.register(
        Remediation(
            vendor="cisco",
            platform="ios",
            control_id=finding.control_id,
            command="no ip http server",
            description="Disable insecure HTTP management.",
            requires_change_window=True,
        )
    )

    generator = RemediationGenerator(registry)

    remediation = generator.generate(
        vendor="cisco",
        platform="ios",
        control_id=finding.control_id,
    )

    assert finding.status == "FAIL"
    assert remediation is not None

    assert remediation.control_id == "MGMT-HTTP-001"
    assert remediation.vendor == "cisco"
    assert remediation.platform == "ios"
    assert remediation.command == "no ip http server"
    assert remediation.requires_change_window is True