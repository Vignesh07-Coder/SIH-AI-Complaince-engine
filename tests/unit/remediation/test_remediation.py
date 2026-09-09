import pytest

from sih26155.remediation.generator import RemediationGenerator
from sih26155.remediation.models import Remediation
from sih26155.remediation.registry import RemediationRegistry
from sih26155.remediation.validators import (
    RemediationValidationError,
    RemediationValidator,
)


def make_remediation(
    command: str = "no ip http server",
) -> Remediation:
    return Remediation(
        vendor="cisco",
        platform="ios",
        control_id="MGMT-HTTP-001",
        command=command,
        description="Disable insecure HTTP management.",
        requires_change_window=True,
    )


def test_valid_remediation_is_accepted():
    remediation = make_remediation()

    assert RemediationValidator.is_valid(remediation) is True


def test_dangerous_remediation_is_rejected():
    remediation = make_remediation(command="reload")

    with pytest.raises(RemediationValidationError):
        RemediationValidator.validate(remediation)


def test_duplicate_remediation_is_rejected():
    registry = RemediationRegistry()
    remediation = make_remediation()

    registry.register(remediation)

    with pytest.raises(ValueError):
        registry.register(remediation)


def test_generator_returns_registered_remediation():
    registry = RemediationRegistry()
    registry.register(make_remediation())

    generator = RemediationGenerator(registry)

    result = generator.generate(
        vendor="cisco",
        platform="ios",
        control_id="MGMT-HTTP-001",
    )

    assert result is not None
    assert result.control_id == "MGMT-HTTP-001"
    assert result.vendor == "cisco"
    assert result.platform == "ios"
    assert result.command == "no ip http server"
    assert result.requires_change_window is True