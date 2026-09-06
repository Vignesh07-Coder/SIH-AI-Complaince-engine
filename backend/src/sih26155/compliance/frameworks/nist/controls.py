"""
NIST compliance control catalogue.

The control IDs are internal SIH26155 project control IDs.
Controls operate on vendor-neutral SBM semantic fields.

Official NIST references can be added to the framework
mapping metadata without changing the SBM contract.
"""


NIST_CONTROLS = {
    "MGMT-SSH-001": {
        "control_id": "MGMT-SSH-001",
        "framework": "NIST",
        "nist_reference": "AC-17",
        "title": "SSH remote access must be secured",
        "semantic_field": "management.ssh.version",
        "description": (
            "Remote access must use an approved secure mechanism."
        ),
        "expected": 2,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },

    "MGMT-TELNET-001": {
        "control_id": "MGMT-TELNET-001",
        "framework": "NIST",
        "nist_reference": "AC-17",
        "title": "Insecure remote access must be disabled",
        "semantic_field": "management.telnet.enabled",
        "description": (
            "Remote access must be controlled and restricted "
            "to approved mechanisms."
        ),
        "expected": False,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },

    "MGMT-HTTP-001": {
        "control_id": "MGMT-HTTP-001",
        "framework": "NIST",
        "nist_reference": "AC-17",
        "title": "Secure remote management access",
        "semantic_field": "management.http.enabled",
        "description": (
            "Remote management access must use approved "
            "secure mechanisms."
        ),
        "expected": False,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },

    "AUTH-LOGIN-001": {
        "control_id": "AUTH-LOGIN-001",
        "framework": "NIST",
        "nist_reference": "IA-2",
        "title": "User identification and authentication",
        "semantic_field": "authentication.login_protection.enabled",
        "description": (
            "Users must be identified and authenticated before "
            "being granted access."
        ),
        "expected": True,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },

    "LOG-001": {
        "control_id": "LOG-001",
        "framework": "NIST",
        "nist_reference": "AU-12",
        "title": "Audit record generation",
        "semantic_field": "logging.enabled",
        "description": (
            "Security-relevant events must generate appropriate "
            "audit records."
        ),
        "expected": True,
        "operator": "eq",
        "severity": "medium",
        "evidence_required": True,
        "remediation_required": True,
    },
}


def get_nist_control(control_id: str):
    """Return a NIST control by internal project control ID."""
    return NIST_CONTROLS.get(control_id)


def get_all_nist_controls():
    """Return all NIST controls."""
    return list(NIST_CONTROLS.values())