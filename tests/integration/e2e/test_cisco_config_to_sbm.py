from pathlib import Path

from sih26155.core.facts.builder import build_security_baseline
from sih26155.core.schema.enums import Vendor
from sih26155.ingestion.detection.vendor_detector import detect_vendor
from sih26155.parsers.cisco.ios import CiscoIOSParser


def test_golden_cisco_config_to_security_baseline():
    config_path = Path("data/configs/cisco/test.conf")
    config = config_path.read_text(encoding="utf-8")

    # Stage 1: deterministic vendor detection
    detection = detect_vendor(config)

    assert detection.vendor == Vendor.CISCO
    assert detection.confidence > 0.0
    assert "hostname " in detection.matched_signatures
    assert "ip ssh " in detection.matched_signatures
    assert "line vty " in detection.matched_signatures

    # Stage 2: vendor-specific parsing
    parser = CiscoIOSParser()
    parse_result = parser.parse(
        config=config,
        source_file=str(config_path),
    )

    assert parse_result.facts
    assert parse_result.evidence

    # Stage 3: normalization into the canonical SBM
    baseline = build_security_baseline(parse_result.facts)

    # Device identity
    assert baseline.device.hostname == "EDGE-01"

    # Management security
    assert baseline.management.ssh.enabled is True
    assert baseline.management.ssh.version == 2
    assert baseline.management.telnet.enabled is False
    assert baseline.management.http.enabled is True

    # Missing controls must remain UNKNOWN/None,
    # not silently become False.
    assert baseline.authentication.login_protection.enabled is None
    assert baseline.logging.enabled is None

    # Stage 4: evidence must survive parsing
    assert len(parse_result.evidence) == len(parse_result.facts)

    evidence_text = [item.raw_text for item in parse_result.evidence]

    assert "hostname EDGE-01" in evidence_text
    assert "ip ssh version 2" in evidence_text
    assert "ip http server" in evidence_text
    assert " transport input ssh" in evidence_text

    # The fixture contains no unsupported commands.
    assert parse_result.unknown_lines == []