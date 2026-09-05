import json
from pathlib import Path

from .models import PolicyRule, PolicySet


class PolicyLoader:
    """Loads compliance policies from JSON files."""

    @staticmethod
    def load_file(path: str | Path) -> PolicySet:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Policy file not found: {file_path}"
            )

        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            rules_data = data.get("controls", [])
            name = data.get("name", file_path.stem)
        elif isinstance(data, list):
            rules_data = data
            name = file_path.stem
        else:
            raise ValueError(
                "Policy file must contain an object or array."
            )

        if not isinstance(rules_data, list):
            raise ValueError("'controls' must be a list.")

        rules = [
            PolicyRule.from_dict(rule)
            for rule in rules_data
        ]

        return PolicySet(
            name=name,
            rules=rules,
        )

    @staticmethod
    def load_directory(path: str | Path) -> list[PolicySet]:
        directory = Path(path)

        if not directory.exists():
            raise FileNotFoundError(
                f"Policy directory not found: {directory}"
            )

        policy_sets = []

        for file_path in sorted(directory.glob("*.json")):
            policy_sets.append(
                PolicyLoader.load_file(file_path)
            )

        return policy_sets