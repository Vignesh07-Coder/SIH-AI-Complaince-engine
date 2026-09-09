from pathlib import Path

from sih26155.core.pipeline.analyze import analyze_config


def test_full_cisco_analysis_pipeline():
    config_path = Path("data/configs/cisco/test.conf")
    config = config_path.read_text(encoding="utf-8")

    result = analyze_config(
        config=config,
        source_file=str(config_path),
    )

    assert result.vendor.vendor.value == "cisco"

    assert result.baseline.device.hostname == "EDGE-01"
    assert result.baseline.management.ssh.version == 2
    assert result.baseline.management.ssh.enabled is True
    assert result.baseline.management.telnet.enabled is False
    assert result.baseline.management.http.enabled is True

    findings = {
        finding.control_id: finding
        for finding in result.findings
    }

    assert findings["MGMT-SSH-001"].status == "PASS"
    assert findings["MGMT-TELNET-001"].status == "PASS"
    assert findings["MGMT-HTTP-001"].status == "FAIL"

    assert findings["AUTH-LOGIN-001"].status == "UNKNOWN"
    assert findings["LOG-001"].status == "UNKNOWN"

    assert len(result.remediations) == 1
    assert result.remediations[0].control_id == "MGMT-HTTP-001"
    assert result.remediations[0].command == "no ip http server"