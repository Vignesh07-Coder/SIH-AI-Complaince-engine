from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Remediation:
    vendor: str
    platform: str
    control_id: str
    command: str
    description: str
    requires_change_window: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)