from pathlib import Path

from sih26155.compliance.evaluator.engine import Finding
from sih26155.remediation.generator import RemediationGenerator
from sih26155.remediation.loader import RemediationLoader
from sih26155.remediation.registry import RemediationRegistry


def test_failed_finding_loads_remediation_from_data():
    registry = RemediationRegistry()

    count = RemediationLoader.load_file(
        Path("data/remediation/cisco/remediations.json"),
        registry,
    )

    assert count == 3
    assert len(registry) == 3

    finding = Finding(
        control_id="MGMT-HTTP-001",
        status="FAIL",
        severity="high",
        description="HTTP management must be disabled.",
        expected=False,
        observed=True,
    )

    generator = RemediationGenerator(registry)

    remediation = generator.generate(
        vendor="cisco",
        platform="ios",
        control_id=finding.control_id,
    )

    assert remediation is not None
    assert remediation.command == "no ip http server"
    assert remediation.control_id == finding.control_id