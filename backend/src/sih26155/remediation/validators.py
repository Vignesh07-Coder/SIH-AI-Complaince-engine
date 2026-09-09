import re

from .models import Remediation


class RemediationValidationError(ValueError):
    """
    Raised when a remediation record fails validation.
    """


class RemediationValidator:
    """
    Validates remediation records before they are registered.

    This validator performs structural and safety checks.
    It never executes commands.
    """

    CONTROL_ID_PATTERN = re.compile(
        r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$"
    )

    ALLOWED_VENDORS = {
        "cisco",
        "juniper",
        "palo alto",
        "palo_alto",
        "fortinet",
        "arista",
        "huawei",
        "aruba",
        "nokia",
        "mikrotik",
    }

    DANGEROUS_PATTERNS = (
        r"\breload\b",
        r"\breboot\b",
        r"\bwrite\s+erase\b",
        r"\berase\s+startup-config\b",
        r"\bformat\b",
        r"\bdelete\s+/force\b",
        r"\bdelete\s+/recursive\b",
        r"\bshutdown\b",
        r"\bpoweroff\b",
    )

    @classmethod
    def validate(cls, remediation: Remediation) -> None:
        if not isinstance(remediation, Remediation):
            raise RemediationValidationError(
                "Expected a Remediation instance."
            )

        cls._validate_vendor(remediation)
        cls._validate_platform(remediation)
        cls._validate_control_id(remediation)
        cls._validate_command(remediation)
        cls._validate_description(remediation)

    @classmethod
    def is_valid(cls, remediation: Remediation) -> bool:
        try:
            cls.validate(remediation)
        except RemediationValidationError:
            return False

        return True

    @classmethod
    def _validate_vendor(cls, remediation: Remediation) -> None:
        vendor = remediation.vendor.strip().lower()

        if not vendor:
            raise RemediationValidationError(
                "Vendor cannot be empty."
            )

        if vendor not in cls.ALLOWED_VENDORS:
            raise RemediationValidationError(
                f"Unsupported vendor: {remediation.vendor}"
            )

    @staticmethod
    def _validate_platform(remediation: Remediation) -> None:
        platform = remediation.platform.strip()

        if not platform:
            raise RemediationValidationError(
                "Platform cannot be empty."
            )

    @classmethod
    def _validate_control_id(cls, remediation: Remediation) -> None:
        control_id = remediation.control_id.strip().upper()

        if not control_id:
            raise RemediationValidationError(
                "Control ID cannot be empty."
            )

        if not cls.CONTROL_ID_PATTERN.fullmatch(control_id):
            raise RemediationValidationError(
                f"Invalid control ID format: {control_id}"
            )

    @classmethod
    def _validate_command(cls, remediation: Remediation) -> None:
        command = remediation.command.strip()

        if not command:
            raise RemediationValidationError(
                "Remediation command cannot be empty."
            )

        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, command, flags=re.IGNORECASE):
                raise RemediationValidationError(
                    "Potentially dangerous command rejected: "
                    f"{command}"
                )

    @staticmethod
    def _validate_description(remediation: Remediation) -> None:
        if not remediation.description.strip():
            raise RemediationValidationError(
                "Remediation description cannot be empty."
            )