import json
from pathlib import Path

from .models import Remediation
from .registry import RemediationRegistry


class RemediationLoader:
    @staticmethod
    def load_file(
        path: str | Path,
        registry: RemediationRegistry,
    ) -> int:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Remediation file not found: {file_path}"
            )

        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "Remediation file must contain a JSON array."
            )

        loaded = 0

        for item in data:
            if not isinstance(item, dict):
                raise ValueError(
                    "Each remediation entry must be an object."
                )

            remediation = Remediation(
                vendor=item["vendor"],
                platform=item["platform"],
                control_id=item["control_id"],
                command=item["command"],
                description=item["description"],
                requires_change_window=bool(
                    item.get("requires_change_window", True)
                ),
            )

            registry.register(remediation)
            loaded += 1

        return loaded