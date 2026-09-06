"""
Unit tests for the AI learning/approval subsystem.

Covers (per spec):
4. Confidence bounds
5. Invalid SBM field rejection
6. Human approval
7. Human edit
8. Human rejection
9. Persistence
10. Reloading learned mappings
"""

import json
from pathlib import Path

import pytest

from sih26155.core.contracts.ai import CandidateMapping
from sih26155.ai.semantic_mapping.candidate_generator import (
    generate_candidates,
    VALID_SBM_FIELDS,
)
from sih26155.ai.confidence.scorer import score_candidate
from sih26155.ai.learning.approval import (
    confirm_candidate,
    edit_candidate,
    reject_candidate,
)
from sih26155.ai.learning import mapping_store


def test_confidence_never_reaches_one():
    candidate = CandidateMapping(field="management.ssh.version", value=2, confidence=0.0, reason="test")
    similar = [({"field": "management.ssh.version", "value": 2}, 1.0)]
    score = score_candidate(candidate, similar)
    assert score < 1.0


def test_confidence_is_low_with_no_evidence():
    candidate = CandidateMapping(field="UNKNOWN", value=None, confidence=0.0, reason="test")
    score = score_candidate(candidate, [])
    assert 0.0 <= score <= 0.3


def test_confidence_always_in_valid_range():
    candidate = CandidateMapping(field="management.ssh.version", value=2, confidence=0.0, reason="test")
    for sim in [0.0, 0.25, 0.5, 0.75, 1.0]:
        similar = [({"field": "management.ssh.version", "value": 2}, sim)]
        score = score_candidate(candidate, similar)
        assert 0.0 <= score <= 1.0


def test_generate_candidates_rejects_invalid_field():
    similar_examples = [
        {"source_text": "some weird command", "field": "made.up.field", "value": True}
    ]
    results = generate_candidates("unknown command", "cisco", similar_examples)
    assert results[0].field == "UNKNOWN"
    assert "not a recognized SBM field" in results[0].reason


def test_generate_candidates_accepts_valid_field():
    similar_examples = [
        {"source_text": "ip ssh version 2", "field": "management.ssh.version", "value": 2}
    ]
    results = generate_candidates("set secure-admin ssh protocol v2", "cisco", similar_examples)
    assert results[0].field == "management.ssh.version"
    assert results[0].field in VALID_SBM_FIELDS


def test_generate_candidates_no_evidence_returns_unknown():
    results = generate_candidates("totally novel syntax", "cisco", [])
    assert results[0].field == "UNKNOWN"


def test_confirm_candidate_persists_mapping(tmp_path, monkeypatch):
    monkeypatch.setattr(mapping_store, "LEARNED_DIR", tmp_path / "learned")

    candidate = CandidateMapping(
        field="management.ssh.version", value=2, confidence=0.91,
        reason="SSH protocol version indicated.",
    )

    result = confirm_candidate(
        candidate, unknown_text="set secure-admin ssh protocol v2",
        context="cisco", approved_by="tester",
    )

    assert result.status == "approved"
    assert result.field == "management.ssh.version"
    assert result.value == 2

    saved_files = list((tmp_path / "learned").glob("*.json"))
    assert len(saved_files) == 1


def test_edit_candidate_with_valid_field_persists(tmp_path, monkeypatch):
    monkeypatch.setattr(mapping_store, "LEARNED_DIR", tmp_path / "learned")

    candidate = CandidateMapping(
        field="UNKNOWN", value=None, confidence=0.2, reason="No match found.",
    )

    result = edit_candidate(
        candidate, unknown_text="disable insecure http mgmt",
        context="cisco", approved_by="tester",
        corrected_field="management.http.enabled", corrected_value=False,
    )

    assert result.status == "approved_edited"
    assert result.field == "management.http.enabled"
    assert result.value is False


def test_edit_candidate_with_invalid_field_is_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(mapping_store, "LEARNED_DIR", tmp_path / "learned")

    candidate = CandidateMapping(field="UNKNOWN", value=None, confidence=0.2, reason="No match.")

    result = edit_candidate(
        candidate, unknown_text="some text", context="cisco", approved_by="tester",
        corrected_field="not.a.real.field", corrected_value=True,
    )

    assert result.status == "rejected"
    assert result.error is not None
    saved_files = list((tmp_path / "learned").glob("*.json")) if (tmp_path / "learned").exists() else []
    assert len(saved_files) == 0


def test_reject_candidate_does_not_persist(tmp_path, monkeypatch):
    monkeypatch.setattr(mapping_store, "LEARNED_DIR", tmp_path / "learned")

    candidate = CandidateMapping(
        field="management.ssh.version", value=2, confidence=0.4, reason="Weak match.",
    )

    result = reject_candidate(candidate)

    assert result.status == "rejected"
    assert result.field is None
    learned_dir = tmp_path / "learned"
    assert not learned_dir.exists() or len(list(learned_dir.glob("*.json"))) == 0


def test_saved_mapping_has_required_fields(tmp_path, monkeypatch):
    monkeypatch.setattr(mapping_store, "LEARNED_DIR", tmp_path / "learned")

    candidate = CandidateMapping(
        field="management.ssh.version", value=2, confidence=0.91, reason="test reason",
    )
    confirm_candidate(candidate, "set secure-admin ssh protocol v2", "cisco", "tester")

    saved_file = next((tmp_path / "learned").glob("*.json"))
    saved = json.loads(saved_file.read_text())

    required_keys = {
        "source_text", "field", "value", "confidence",
        "status", "approved_by", "context", "created_at",
    }
    assert required_keys.issubset(saved.keys())


def test_load_all_learned_returns_saved_mappings(tmp_path, monkeypatch):
    monkeypatch.setattr(mapping_store, "LEARNED_DIR", tmp_path / "learned")

    candidate = CandidateMapping(
        field="management.telnet.enabled", value=False, confidence=0.85, reason="test",
    )
    confirm_candidate(candidate, "no telnet-server", "juniper", "tester")

    loaded = mapping_store.load_all_learned()
    assert len(loaded) == 1
    assert loaded[0]["field"] == "management.telnet.enabled"


def test_load_all_learned_empty_when_no_mappings(tmp_path, monkeypatch):
    monkeypatch.setattr(mapping_store, "LEARNED_DIR", tmp_path / "learned_empty")
    loaded = mapping_store.load_all_learned()
    assert loaded == []