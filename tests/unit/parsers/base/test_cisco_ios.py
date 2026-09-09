from sih26155.parsers.cisco.ios import CiscoIOSParser


CONFIG = """\
hostname EDGE-01
!
ip ssh version 2
ip http server
!
line vty 0 4
 transport input ssh
 login local
 exec-timeout 5 0
!
"""


def test_cisco_ios_parser_extracts_core_security_facts():
    parser = CiscoIOSParser()

    result = parser.parse(
        config=CONFIG,
        source_file="test.conf",
    )

    fields = {
        fact.field: fact.value
        for fact in result.facts
    }

    assert fields["device.hostname"] == "EDGE-01"
    assert fields["management.ssh.version"] == 2
    assert fields["management.http.enabled"] is True

    assert fields["management.ssh.enabled"] is True
    assert fields["management.telnet.enabled"] is False

    assert fields["management.vty.login_mode"] == "local"

    assert fields["management.vty.exec_timeout"] == {
        "minutes": 5,
        "seconds": 0,
    }


def test_cisco_ios_parser_creates_evidence():
    parser = CiscoIOSParser()

    result = parser.parse(
        config="hostname EDGE-01\n",
        source_file="test.conf",
    )

    assert len(result.facts) == 1
    assert len(result.evidence) == 1

    fact = result.facts[0]
    evidence = result.evidence[0]

    assert fact.field == "device.hostname"
    assert fact.value == "EDGE-01"

    assert fact.evidence_id == "evidence:cisco-ios:test.conf:1"

    assert evidence.source_file == "test.conf"
    assert evidence.raw_text == "hostname EDGE-01"
    assert evidence.line_number == 1
    assert evidence.parser == "cisco-ios"


def test_cisco_ios_parser_preserves_unknown_lines():
    parser = CiscoIOSParser()

    config = """\
hostname EDGE-01
some-future-cisco-command whatever
"""

    result = parser.parse(
        config=config,
        source_file="test.conf",
    )

    assert "some-future-cisco-command whatever" in result.unknown_lines


def test_cisco_ios_parser_handles_http_negation():
    parser = CiscoIOSParser()

    result = parser.parse(
        config="no ip http server\n",
        source_file="test.conf",
    )

    fields = {
        fact.field: fact.value
        for fact in result.facts
    }

    assert fields["management.http.enabled"] is False


def test_cisco_ios_parser_extracts_login_protection():
    parser = CiscoIOSParser()

    result = parser.parse(
        config="login block-for 120 attempts 3 within 60\n",
        source_file="test.conf",
    )

    fields = {
        fact.field: fact.value
        for fact in result.facts
    }

    assert fields["authentication.login_protection"] == {
        "enabled": True,
        "block_seconds": 120,
        "attempts": 3,
        "window_seconds": 60,
    }


def test_cisco_ios_parser_transport_ssh_enables_only_ssh():
    config = """
line vty 0 4
 transport input ssh
!
"""

    parser = CiscoIOSParser()
    result = parser.parse(config, "transport-ssh.conf")

    facts = {fact.field: fact.value for fact in result.facts}

    assert facts["management.ssh.enabled"] is True
    assert facts["management.telnet.enabled"] is False


def test_cisco_ios_parser_transport_telnet_ssh_enables_both():
    config = """
line vty 0 4
 transport input telnet ssh
!
"""

    parser = CiscoIOSParser()
    result = parser.parse(config, "transport-telnet-ssh.conf")

    facts = {fact.field: fact.value for fact in result.facts}

    assert facts["management.ssh.enabled"] is True
    assert facts["management.telnet.enabled"] is True


def test_cisco_ios_parser_transport_none_disables_ssh_and_telnet():
    config = """
line vty 0 4
 transport input none
!
"""

    parser = CiscoIOSParser()
    result = parser.parse(config, "transport-none.conf")

    facts = {fact.field: fact.value for fact in result.facts}

    assert facts["management.ssh.enabled"] is False
    assert facts["management.telnet.enabled"] is False

    def test_cisco_ios_parser_transport_ssh_enables_only_ssh():
        config = """
line vty 0 4
 transport input ssh
!
"""

        parser = CiscoIOSParser()
        result = parser.parse(config, "transport-ssh.conf")

    facts = {fact.field: fact.value for fact in result.facts}

    assert facts["management.ssh.enabled"] is True
    assert facts["management.telnet.enabled"] is False


def test_cisco_ios_parser_transport_telnet_ssh_enables_both():
    config = """
line vty 0 4
 transport input telnet ssh
!
"""

    parser = CiscoIOSParser()
    result = parser.parse(config, "transport-telnet-ssh.conf")

    facts = {fact.field: fact.value for fact in result.facts}

    assert facts["management.ssh.enabled"] is True
    assert facts["management.telnet.enabled"] is True


def test_cisco_ios_parser_transport_none_disables_ssh_and_telnet():
    config = """
line vty 0 4
 transport input none
!
"""

    parser = CiscoIOSParser()
    result = parser.parse(config, "transport-none.conf")

    facts = {fact.field: fact.value for fact in result.facts}

    assert facts["management.ssh.enabled"] is False
    assert facts["management.telnet.enabled"] is False