from sih26155.core.facts.builder import build_security_baseline
from sih26155.parsers.cisco.ios import CiscoIOSParser


def test_cisco_ios_parser_to_security_baseline():
    config = """
hostname EDGE-01
!
ip ssh version 2
no ip http server
!
line vty 0 4
 transport input ssh
 login local
 exec-timeout 5 0
!
login block-for 120 attempts 3 within 60
logging buffered 16384
!
"""

    parser = CiscoIOSParser()

    parse_result = parser.parse(
        config=config,
        source_file="edge-01.conf",
    )

    baseline = build_security_baseline(parse_result.facts)

    assert baseline.device.hostname == "EDGE-01"

    assert baseline.management.ssh.enabled is True
    assert baseline.management.ssh.version == 2

    assert baseline.management.telnet.enabled is False
    assert baseline.management.http.enabled is False

    assert baseline.authentication.login_protection.enabled is True
    assert baseline.authentication.login_protection.block_seconds == 120
    assert baseline.authentication.login_protection.attempts == 3
    assert baseline.authentication.login_protection.window_seconds == 60

    assert baseline.logging.enabled is True