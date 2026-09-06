from dataclasses import dataclass
from typing import Optional

from .models import Remediation
from .registry import RemediationRegistry


@dataclass(frozen=True)
class RemediationResult:
    """
    Result returned after generating a remediation.
    """

    control_id: str
    vendor: str
    platform: str
    command: str
    description: str
    requires_change_window: bool


class RemediationGenerator:
    """
    Generates remediation instructions from the validated registry.

    The generator does not create arbitrary vendor commands.
    It retrieves commands that have already been registered.
    """

    def __init__(self, registry: RemediationRegistry) -> None:
        self.registry = registry

    def generate(
        self,
        vendor: str,
        platform: str,
        control_id: str,
    ) -> Optional[RemediationResult]:
        """
        Generate remediation for a specific vendor,
        platform and compliance control.

        Returns None when no remediation is registered.
        """

        remediation = self.registry.get(
            vendor=vendor,
            platform=platform,
            control_id=control_id,
        )

        if remediation is None:
            return None

        return self._build_result(remediation)

    def generate_required(
        self,
        vendor: str,
        platform: str,
        control_id: str,
    ) -> RemediationResult:
        """
        Generate remediation and raise an error if
        no validated remediation exists.
        """

        remediation = self.registry.require(
            vendor=vendor,
            platform=platform,
            control_id=control_id,
        )

        return self._build_result(remediation)

    @staticmethod
    def _build_result(
        remediation: Remediation,
    ) -> RemediationResult:
        """
        Convert a Remediation model into a result object.
        """

        return RemediationResult(
            control_id=remediation.control_id,
            vendor=remediation.vendor,
            platform=remediation.platform,
            command=remediation.command,
            description=remediation.description,
            requires_change_window=(
                remediation.requires_change_window
            ),
        )

    def generate_for_findings(
        self,
        vendor: str,
        platform: str,
        control_ids: list[str],
    ) -> list[RemediationResult]:
        """
        Generate remediation results for multiple controls.

        Controls without a registered remediation are skipped.
        """

        results: list[RemediationResult] = []

        for control_id in control_ids:
            result = self.generate(
                vendor=vendor,
                platform=platform,
                control_id=control_id,
            )

            if result is not None:
                results.append(result)

        return results