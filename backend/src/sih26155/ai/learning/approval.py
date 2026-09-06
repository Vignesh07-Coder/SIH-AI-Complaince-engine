from dataclasses import dataclass
from datetime import datetime, timezone

from sih26155.core.contracts.ai import CandidateMapping
from sih26155.ai.semantic_mapping.candidate_generator import VALID_SBM_FIELDS
from sih26155.ai.learning.mapping_store import save_approved_mapping


@dataclass
class ApprovalResult:
    status: str  # "approved", "approved_edited", "rejected"
    field: str | None
    value: object | None
    original_candidate: CandidateMapping
    error: str | None = None


def confirm_candidate(
    candidate: CandidateMapping,
    unknown_text: str,
    context: str,
    approved_by: str,
) -> ApprovalResult:
    """Approve a candidate exactly as the AI proposed it."""
    return _finalize(
        candidate=candidate,
        field=candidate.field,
        value=candidate.value,
        unknown_text=unknown_text,
        context=context,
        approved_by=approved_by,
        status="approved",
    )


def edit_candidate(
    candidate: CandidateMapping,
    unknown_text: str,
    context: str,
    approved_by: str,
    corrected_field: str,
    corrected_value: object,
) -> ApprovalResult:
    """Approve a candidate after a human correction to field and/or value."""
    if corrected_field not in VALID_SBM_FIELDS:
        return ApprovalResult(
            status="rejected",
            field=None,
            value=None,
            original_candidate=candidate,
            error=f"'{corrected_field}' is not a valid SBM field.",
        )

    return _finalize(
        candidate=candidate,
        field=corrected_field,
        value=corrected_value,
        unknown_text=unknown_text,
        context=context,
        approved_by=approved_by,
        status="approved_edited",
    )


def reject_candidate(candidate: CandidateMapping) -> ApprovalResult:
    """Reject a candidate outright. Nothing is persisted."""
    return ApprovalResult(
        status="rejected",
        field=None,
        value=None,
        original_candidate=candidate,
    )


def _finalize(
    candidate: CandidateMapping,
    field: str,
    value: object,
    unknown_text: str,
    context: str,
    approved_by: str,
    status: str,
) -> ApprovalResult:
    mapping = {
        "source_text": unknown_text,
        "field": field,
        "value": value,
        "confidence": candidate.confidence,
        "status": status,
        "approved_by": approved_by,
        "context": context,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    save_approved_mapping(mapping)

    return ApprovalResult(
        status=status,
        field=field,
        value=value,
        original_candidate=candidate,
    )