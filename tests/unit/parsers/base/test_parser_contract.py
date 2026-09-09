from sih26155.core.evidence.models import Evidence
from sih26155.core.facts.models import SecurityFact
from sih26155.core.contracts.parser import ParseResult, VendorParser


def test_parse_result_uses_canonical_models():
    fact = SecurityFact(
        field="management.ssh.version",
        value=2,
    )

    evidence = Evidence(
        source_file="test.conf",
        raw_text="ip ssh version 2",
        line_number=1,
        parser="cisco-ios",
    )

    result = ParseResult(
        facts=[fact],
        evidence=[evidence],
        unknown_lines=[],
    )

    assert result.facts[0] is fact
    assert result.evidence[0] is evidence
    assert result.unknown_lines == []


def test_vendor_parser_contract_exists():
    assert VendorParser is not None