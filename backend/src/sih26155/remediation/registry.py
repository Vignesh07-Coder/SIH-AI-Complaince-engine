from typing import Optional

from .models import Remediation
from .validators import RemediationValidator


class RemediationRegistry:
    """
    Registry of validated vendor-specific remediation commands.

    Remediation records are validated before they are stored.
    The compliance engine remains vendor-neutral.
    """

    def __init__(self) -> None:
        self._remediations: dict[
            tuple[str, str, str],
            Remediation,
        ] = {}

    @staticmethod
    def _make_key(
        vendor: str,
        platform: str,
        control_id: str,
    ) -> tuple[str, str, str]:
        """
        Create a normalized registry key.
        """

        return (
            vendor.strip().lower(),
            platform.strip().lower(),
            control_id.strip().upper(),
        )

    def register(self, remediation: Remediation) -> None:
        """
        Validate and register a remediation command.

        Raises:
            RemediationValidationError:
                If the remediation is invalid.

            ValueError:
                If a remediation already exists for the
                same vendor, platform and control.
        """

        # Validate before storing.
        RemediationValidator.validate(remediation)

        key = self._make_key(
            vendor=remediation.vendor,
            platform=remediation.platform,
            control_id=remediation.control_id,
        )

        if key in self._remediations:
            raise ValueError(
                "Remediation already registered for "
                f"{remediation.vendor} / "
                f"{remediation.platform} / "
                f"{remediation.control_id}"
            )

        self._remediations[key] = remediation

    def get(
        self,
        vendor: str,
        platform: str,
        control_id: str,
    ) -> Optional[Remediation]:
        """
        Retrieve a remediation.

        Returns:
            Remediation if found, otherwise None.
        """

        key = self._make_key(
            vendor=vendor,
            platform=platform,
            control_id=control_id,
        )

        return self._remediations.get(key)

    def require(
        self,
        vendor: str,
        platform: str,
        control_id: str,
    ) -> Remediation:
        """
        Retrieve a remediation.

        Raises:
            KeyError:
                If no remediation is registered.
        """

        remediation = self.get(
            vendor=vendor,
            platform=platform,
            control_id=control_id,
        )

        if remediation is None:
            raise KeyError(
                "No remediation registered for "
                f"{vendor} / {platform} / {control_id}"
            )

        return remediation

    def remove(
        self,
        vendor: str,
        platform: str,
        control_id: str,
    ) -> bool:
        """
        Remove a remediation from the registry.

        Returns:
            True if removed, otherwise False.
        """

        key = self._make_key(
            vendor=vendor,
            platform=platform,
            control_id=control_id,
        )

        if key not in self._remediations:
            return False

        del self._remediations[key]
        return True

    def list_all(self) -> list[Remediation]:
        """
        Return all registered remediations.
        """

        return list(self._remediations.values())

    def list_for_vendor(
        self,
        vendor: str,
        platform: Optional[str] = None,
    ) -> list[Remediation]:
        """
        Return remediations for a vendor.

        If platform is provided, only that platform is returned.
        """

        vendor_name = vendor.strip().lower()

        if platform is not None:
            platform_name = platform.strip().lower()

            return [
                remediation
                for remediation in self._remediations.values()
                if (
                    remediation.vendor.strip().lower()
                    == vendor_name
                    and remediation.platform.strip().lower()
                    == platform_name
                )
            ]

        return [
            remediation
            for remediation in self._remediations.values()
            if remediation.vendor.strip().lower()
            == vendor_name
        ]

    def clear(self) -> None:
        """
        Remove all registered remediations.
        """

        self._remediations.clear()

    def __len__(self) -> int:
        """
        Return the number of registered remediations.
        """

        return len(self._remediations)
