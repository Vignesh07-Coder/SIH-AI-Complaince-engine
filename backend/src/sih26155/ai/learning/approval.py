from sih26155.core.contracts.ai import CandidateMapping
from sih26155.ai.learning.mapping_store import save_approved_mapping
from sih26155.ai.learning.versioning import record_version


def review_candidate(candidate: CandidateMapping, unknown_text: str, reviewer: str = "unknown") -> bool:
    """
    Terminal-based human review: Confirm / Edit / Reject.
    Returns True if approved (as-is or edited), False if rejected.
    """
    print(f"\nField: {candidate.field}")
    print(f"Value: {candidate.value}")
    print(f"Confidence: {candidate.confidence}")
    print(f"Reason: {candidate.reason}")

    if candidate.confidence > 0.9:
        decision = input("High confidence. Confirm? (y/n): ").strip().lower()
        if decision == "y":
            _approve(candidate, candidate.field, candidate.value, unknown_text, reviewer, was_edited=False)
            return True
        print("Rejected.")
        return False

    decision = input("Approve / Edit / Reject? (a/e/r): ").strip().lower()

    if decision == "a":
        _approve(candidate, candidate.field, candidate.value, unknown_text, reviewer, was_edited=False)
        return True
    elif decision == "e":
        new_field = input(f"Correct field (was '{candidate.field}'): ").strip()
        new_value = input(f"Correct value (was '{candidate.value}'): ").strip()
        _approve(candidate, new_field, new_value, unknown_text, reviewer, was_edited=True)
        return True

    print("Rejected.")
    return False


def _approve(candidate, field, value, unknown_text, reviewer, was_edited):
    mapping = {
        "source_text": unknown_text,
        "field": field,
        "value": value,
        "confidence": candidate.confidence,
        "status": "approved_edited" if was_edited else "approved",
        "approved_by": reviewer,
    }
    save_approved_mapping(mapping)
    record_version(field.replace(".", "_"), mapping)
    print("Saved.")