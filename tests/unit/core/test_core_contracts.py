# tests/unit/core/test_core_contracts.py

from sih26155.core.schema.models import (
    SecurityBaseline,
    DeviceInfo,
    ManagementConfig,
    AuthenticationConfig,
    LoggingConfig,
)

from sih26155.core.schema.enums import (
    Vendor,
    ConfidenceSource,
    FindingStatus,
    Severity,
)

from sih26155.core.facts.models import SecurityFact

from sih26155.core.evidence.models import Evidence

from sih26155.core.contracts.parser import ParseResult
from sih26155.core.contracts.ai import CandidateMapping
from sih26155.core.contracts.compliance import Finding
from sih26155.core.contracts.remediation import Remediation


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

def test_security_baseline_can_be_created_with_defaults():
    baseline = SecurityBaseline()

    assert baseline.device is not None
    assert baseline.management is not None
    assert baseline.authentication is not None
    assert baseline.logging is not None


def test_security_baseline_contains_expected_nested_sections():
    baseline = SecurityBaseline()

    assert isinstance(baseline.device, DeviceInfo)
    assert isinstance(baseline.management, ManagementConfig)
    assert isinstance(baseline.authentication, AuthenticationConfig)
    assert isinstance(baseline.logging, LoggingConfig)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

def test_vendor_enum_contains_supported_vendors():
    assert Vendor.CISCO.value == "cisco"
    assert Vendor.JUNIPER.value == "juniper"
    assert Vendor.PALO_ALTO.value == "paloalto"
    assert Vendor.UNKNOWN.value == "unknown"


def test_confidence_source_enum_is_stable():
    assert ConfidenceSource.DETERMINISTIC.value == "deterministic"
    assert ConfidenceSource.AI.value == "ai"
    assert ConfidenceSource.HUMAN.value == "human"


def test_finding_status_enum_is_stable():
    assert FindingStatus.PASS.value == "pass"
    assert FindingStatus.FAIL.value == "fail"
    assert FindingStatus.UNKNOWN.value == "unknown"


def test_severity_enum_is_stable():
    assert Severity.INFO.value == "info"
    assert Severity.LOW.value == "low"
    assert Severity.MEDIUM.value == "medium"
    assert Severity.HIGH.value == "high"
    assert Severity.CRITICAL.value == "critical"


# ---------------------------------------------------------------------------
# Security Facts
# ---------------------------------------------------------------------------

def test_security_fact_preserves_semantic_fact_and_confidence():
    fact = SecurityFact(
        field="management.ssh.version",
        value=2,
        confidence=1.0,
        source=ConfidenceSource.DETERMINISTIC,
    )

    assert fact.field == "management.ssh.version"
    assert fact.value == 2
    assert fact.confidence == 1.0
    assert fact.source == ConfidenceSource.DETERMINISTIC


# ---------------------------------------------------------------------------
# Evidence
# ---------------------------------------------------------------------------

def test_evidence_preserves_source_information():
    evidence = Evidence(
        source_file="router01.cfg",
        line_number=42,
        raw_text="ip ssh version 2",
        parser="cisco_ios",
        confidence=1.0,
    )

    assert evidence.source_file == "router01.cfg"
    assert evidence.line_number == 42
    assert evidence.raw_text == "ip ssh version 2"
    assert evidence.parser == "cisco_ios"
    assert evidence.confidence == 1.0


# ---------------------------------------------------------------------------
# Parser contract
# ---------------------------------------------------------------------------

def test_parse_result_can_carry_facts_and_unknown_lines():
    fact = SecurityFact(
        field="management.ssh.version",
        value=2,
    )

    result = ParseResult(
        facts=[fact],
        unknown_lines=["some unknown command"],
    )

    assert len(result.facts) == 1
    assert result.facts[0] == fact
    assert result.unknown_lines == ["some unknown command"]


# ---------------------------------------------------------------------------
# AI contract
# ---------------------------------------------------------------------------

def test_candidate_mapping_preserves_ai_proposal():
    candidate = CandidateMapping(
        field="management.ssh.version",
        value=2,
        confidence=0.91,
        reason="Command semantics indicate SSH version 2.",
    )

    assert candidate.field == "management.ssh.version"
    assert candidate.value == 2
    assert candidate.confidence == 0.91
    assert candidate.reason


# ---------------------------------------------------------------------------
# Compliance contract
# ---------------------------------------------------------------------------

def test_finding_preserves_compliance_result():
    finding = Finding(
        control_id="SSH-001",
        status=FindingStatus.PASS,
        severity=Severity.HIGH,
        description="SSH must use version 2.",
        expected=2,
        observed=2,
        evidence=[],
    )

    assert finding.control_id == "SSH-001"
    assert finding.status == FindingStatus.PASS
    assert finding.severity == Severity.HIGH
    assert finding.expected == 2
    assert finding.observed == 2
    assert finding.evidence == []


# ---------------------------------------------------------------------------
# Remediation contract
# ---------------------------------------------------------------------------

def test_remediation_preserves_vendor_specific_instructions():
    remediation = Remediation(
        control_id="SSH-001",
        vendor="cisco",
        platform="ios",
        instructions="Enable SSH version 2.",
        commands=["ip ssh version 2"],
    )

    assert remediation.control_id == "SSH-001"
    assert remediation.vendor == "cisco"
    assert remediation.platform == "ios"
    assert remediation.commands == ["ip ssh version 2"]