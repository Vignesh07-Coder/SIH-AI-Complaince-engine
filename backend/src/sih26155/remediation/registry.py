from typing import Optional

from .models import Remediation


class RemediationRegistry:
    """
    Registry of validated vendor-specific remediation commands.

    The compliance engine remains vendor-neutral.
    Vendor-specific commands are stored here.
    """

    def __init__(self) -> None:
        self._remediations: dict[
            tuple[str, str, str],
            Remediation,
        ] = {}

    def register(self, remediation: Remediation) -> None:
        """
        Register a remediation command.

        Key:
            (vendor, platform, control_id)
        """

        key = (
            remediation.vendor.lower(),
            remediation.platform.lower(),
            remediation.control_id.upper(),
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
        Retrieve a remediation for a vendor, platform and control.
        """

        key = (
            vendor.lower(),
            platform.lower(),
            control_id.upper(),
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
            KeyError if no remediation is registered.
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

        key = (
            vendor.lower(),
            platform.lower(),
            control_id.upper(),
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

        vendor_name = vendor.lower()

        if platform is not None:
            platform_name = platform.lower()

            return [
                remediation
                for remediation in self._remediations.values()
                if (
                    remediation.vendor.lower() == vendor_name
                    and remediation.platform.lower() == platform_name
                )
            ]

        return [
            remediation
            for remediation in self._remediations.values()
            if remediation.vendor.lower() == vendor_name
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