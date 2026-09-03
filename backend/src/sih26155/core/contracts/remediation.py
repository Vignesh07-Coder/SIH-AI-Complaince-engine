from typing import Protocol


class Remediation:
    def __init__(
        self,
        control_id: str,
        vendor: str,
        platform: str | None,
        instructions: str,
        commands: list[str],
    ):
        self.control_id = control_id
        self.vendor = vendor
        self.platform = platform
        self.instructions = instructions
        self.commands = commands


class RemediationProvider(Protocol):

    def get_remediation(
        self,
        control_id: str,
        vendor: str,
        platform: str | None,
    ) -> Remediation | None:
        ...