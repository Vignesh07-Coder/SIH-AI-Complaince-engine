from pathlib import Path

from sih26155.remediation.loader import RemediationLoader
from sih26155.remediation.registry import RemediationRegistry


def test_loader_registers_remediation_data(tmp_path: Path):
    data_file = tmp_path / "remediations.json"

    data_file.write_text(
        """
        [
          {
            "vendor": "cisco",
            "platform": "ios",
            "control_id": "MGMT-HTTP-001",
            "command": "no ip http server",
            "description": "Disable HTTP management.",
            "requires_change_window": true
          }
        ]
        """,
        encoding="utf-8",
    )

    registry = RemediationRegistry()

    loaded = RemediationLoader.load_file(
        data_file,
        registry,
    )

    assert loaded == 1
    assert len(registry) == 1

    remediation = registry.get(
        vendor="cisco",
        platform="ios",
        control_id="MGMT-HTTP-001",
    )

    assert remediation is not None
    assert remediation.command == "no ip http server"