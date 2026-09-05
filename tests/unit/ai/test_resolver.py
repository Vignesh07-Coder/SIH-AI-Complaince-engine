from sih26155.ai.retrieval.mapping_index import MappingIndex
from sih26155.ai.retrieval.retriever import Retriever
from sih26155.ai.semantic_mapping.resolver import DefaultSemanticResolver


def test_resolve_unknown_ssh_command(tmp_path):
    index = MappingIndex(vendor_dir=str(tmp_path / "vendor"), learned_dir=str(tmp_path / "learned"))
    retriever = Retriever(index)
    resolver = DefaultSemanticResolver(retriever)

    results = resolver.resolve(
        unknown_text="set secure-admin ssh protocol v2",
        context="cisco",
    )

    assert len(results) >= 1
    assert results[0].field is not None
    assert 0.0 <= results[0].confidence <= 1.0
    assert results[0].reason


def test_resolve_matches_known_ssh_pattern(tmp_path):
    vendor_dir = tmp_path / "vendor"
    vendor_dir.mkdir()
    (vendor_dir / "cisco_ssh.json").write_text(
        '[{"source_text": "ip ssh version 2", "field": "management.ssh.version", "value": 2}]'
    )

    index = MappingIndex(vendor_dir=str(vendor_dir), learned_dir=str(tmp_path / "learned"))
    retriever = Retriever(index)
    resolver = DefaultSemanticResolver(retriever)

    results = resolver.resolve(
        unknown_text="set secure-admin ssh protocol v2",
        context="cisco",
    )

    assert results[0].field == "management.ssh.version"
    assert results[0].value == 2
    assert results[0].confidence > 0.3
