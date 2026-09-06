from pathlib import Path

import pytest

from sih26155.ingestion.loaders.file_loader import (
    ConfigurationLoadError,
    load_config,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
TEST_CONFIG = PROJECT_ROOT / "data" / "configs" / "cisco" / "test.conf"


def test_load_config():
    config = load_config(TEST_CONFIG)

    assert config.source_file == "test.conf"
    assert "hostname EDGE-01" in config.content
    assert "ip ssh version 2" in config.content


def test_load_missing_config():
    missing_file = PROJECT_ROOT / "data" / "configs" / "cisco" / "does-not-exist.conf"

    with pytest.raises(ConfigurationLoadError):
        load_config(missing_file)