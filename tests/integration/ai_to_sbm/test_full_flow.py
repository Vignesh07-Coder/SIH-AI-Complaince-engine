"""
Integration test: proves the full AI-to-SBM pipeline works end-to-end,
matching the spec's exact "Final Definition of Done" demo:

unknown command -> semantic retrieval -> candidate mapping -> confidence
-> human CONFIRM -> mapping stored -> same command appears again
-> mapping retrieved -> SBM-compatible semantic fact
"""

from sih26155.core.contracts.ai import CandidateMapping
from sih26155.core.facts.models import SecurityFact
from sih26155.core.schema.enums import ConfidenceSource

from sih26155.ai.retrieval.mapping_index import MappingIndex
from sih26155.ai.retrieval.retriever import Retriever
from sih26155.ai.semantic_mapping.resolver import DefaultSemanticResolver
from sih26155.ai.learning.approval import confirm_candidate
from sih26155.ai.learning import mapping_store


def _candidate_to_fact(candidate: CandidateMapping, evidence_id: str | None = None) -> SecurityFact:
    """
    Local helper for this test only, proving an approved AI candidate
    can become a valid SBM SecurityFact. The real conversion function
    lives wherever Member 1's pipeline wiring calls it.
    """
    return SecurityFact(
        field=candidate.field,
        value=candidate.value,
        confidence=candidate.confidence,
        source=ConfidenceSource.AI,
        evidence_id=evidence_id,
    )


def test_full_ai_to_sbm_pipeline(tmp_path, monkeypatch):
    vendor_dir = tmp_path / "vendor"
    learned_dir = tmp_path / "learned"
    vendor_dir.mkdir()

    (vendor_dir / "cisco_ssh.json").write_text(
        '[{"source_text": "ip ssh version 2", '
        '"field": "management.ssh.version", "value": 2}]'
    )

    monkeypatch.setattr(mapping_store, "LEARNED_DIR", learned_dir)

    unknown_text = "set secure-admin ssh protocol v2"
    context = "cisco"

    # --- First run: nothing learned yet, only vendor data exists ---
    index = MappingIndex(vendor_dir=str(vendor_dir), learned_dir=str(learned_dir))
    retriever = Retriever(index)
    resolver = DefaultSemanticResolver(retriever)

    first_results = resolver.resolve(unknown_text, context)
    assert len(first_results) >= 1

    best_candidate = first_results[0]
    assert best_candidate.field == "management.ssh.version"
    assert best_candidate.value == 2
    assert 0.0 < best_candidate.confidence < 1.0

    # --- Human reviews and confirms the candidate ---
    approval_result = confirm_candidate(
        best_candidate,
        unknown_text=unknown_text,
        context=context,
        approved_by="tester",
    )
    assert approval_result.status == "approved"

    # --- Mapping must now be persisted and reloadable ---
    learned_mappings = mapping_store.load_all_learned()
    assert len(learned_mappings) == 1
    assert learned_mappings[0]["field"] == "management.ssh.version"

    # --- Second run: rebuild the index so it picks up the new learned mapping ---
    index_after_learning = MappingIndex(vendor_dir=str(vendor_dir), learned_dir=str(learned_dir))
    retriever_after_learning = Retriever(index_after_learning)
    resolver_after_learning = DefaultSemanticResolver(retriever_after_learning)

    second_results = resolver_after_learning.resolve(unknown_text, context)
    assert second_results[0].field == "management.ssh.version"
    assert second_results[0].value == 2

    # The exact same command was now seen before -> should score at least
    # as confidently the second time (ideally more, since it's an exact match).
    assert second_results[0].confidence >= best_candidate.confidence

    # --- Prove the approved candidate is SBM-compatible ---
    fact = _candidate_to_fact(second_results[0], evidence_id="test-evidence-1")
    assert isinstance(fact, SecurityFact)
    assert fact.field == "management.ssh.version"
    assert fact.value == 2
    assert fact.source == ConfidenceSource.AI


def test_ai_never_produces_compliance_verdict():
    """
    Explicit boundary check: CandidateMapping must never carry a
    compliance verdict field. This guards the project's core rule.
    """
    candidate = CandidateMapping(
        field="management.http.enabled", value=True, confidence=0.8, reason="test",
    )
    forbidden_attrs = ("status", "pass_fail", "severity", "is_violation", "compliant")
    for attr in forbidden_attrs:
        assert not hasattr(candidate, attr)