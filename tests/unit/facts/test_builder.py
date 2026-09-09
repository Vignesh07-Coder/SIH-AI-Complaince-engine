from sih26155.core.facts.builder import build_security_baseline
from sih26155.core.facts.models import SecurityFact
from sih26155.core.schema.models import SecurityBaseline


def test_builder_returns_security_baseline():
    facts = [
        SecurityFact(
            field="device.hostname",
            value="EDGE-01",
        )
    ]

    baseline = build_security_baseline(facts)

    assert isinstance(baseline, SecurityBaseline)
    assert baseline.device.hostname == "EDGE-01"


def test_builder_maps_management_facts():
    facts = [
        SecurityFact(
            field="management.ssh.enabled",
            value=True,
        ),
        SecurityFact(
            field="management.ssh.version",
            value=2,
        ),
        SecurityFact(
            field="management.telnet.enabled",
            value=False,
        ),
        SecurityFact(
            field="management.http.enabled",
            value=True,
        ),
    ]

    baseline = build_security_baseline(facts)

    assert baseline.management.ssh.enabled is True
    assert baseline.management.ssh.version == 2
    assert baseline.management.telnet.enabled is False
    assert baseline.management.http.enabled is True


def test_builder_maps_login_protection():
    facts = [
        SecurityFact(
            field="authentication.login_protection",
            value={
                "enabled": True,
                "block_seconds": 120,
                "attempts": 3,
                "window_seconds": 60,
            },
        )
    ]

    baseline = build_security_baseline(facts)

    assert baseline.authentication.login_protection.enabled is True
    assert baseline.authentication.login_protection.block_seconds == 120
    assert baseline.authentication.login_protection.attempts == 3
    assert baseline.authentication.login_protection.window_seconds == 60


def test_builder_maps_logging():
    facts = [
        SecurityFact(
            field="logging.enabled",
            value=True,
        )
    ]

    baseline = build_security_baseline(facts)

    assert baseline.logging.enabled is True


def test_builder_preserves_unknown_fields_without_crashing():
    facts = [
        SecurityFact(
            field="some.future.field",
            value="whatever",
        )
    ]

    baseline = build_security_baseline(facts)

    assert isinstance(baseline, SecurityBaseline)


def test_builder_preserves_unknown_values_as_none():
    facts = [
        SecurityFact(
            field="device.hostname",
            value="EDGE-01",
        )
    ]

    baseline = build_security_baseline(facts)

    assert baseline.management.ssh.enabled is None
    assert baseline.management.ssh.version is None
    assert baseline.management.telnet.enabled is None
    assert baseline.management.http.enabled is None
    assert baseline.logging.enabled is None