"""
NIST SP 800-53 compliance control catalogue.

Vendor-neutral SIH26155 controls mapped to NIST
security and privacy control families.
"""

NIST_CONTROLS = {
    "MGMT-SSH-001": {
        "control_id": "MGMT-SSH-001",
        "framework": "NIST",
        "nist_reference": "AC-17",
        "title": "Secure remote access",
        "semantic_field": "management.ssh.version",
        "description": (
            "Remote access must use approved and secure "
            "communication mechanisms."
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
        "title": "Restrict insecure remote access",
        "semantic_field": "management.telnet.enabled",
        "description": (
            "Insecure remote access mechanisms must be disabled."
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
        "title": "Secure remote management",
        "semantic_field": "management.http.enabled",
        "description": (
            "Insecure remote management access must be disabled."
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
        "title": "Identification and authentication",
        "semantic_field": "authentication.login_protection.enabled",
        "description": (
            "Authentication protection must be enabled before "
            "management access is granted."
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
            "Security-relevant events must be logged."
        ),
        "expected": True,
        "operator": "eq",
        "severity": "medium",
        "evidence_required": True,
        "remediation_required": True,
    },
}


def get_nist_control(control_id: str):
    return NIST_CONTROLS.get(control_id)


def get_all_nist_controls():
    return list(NIST_CONTROLS.values())
