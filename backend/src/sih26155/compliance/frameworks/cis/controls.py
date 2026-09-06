"""
CIS compliance control catalogue.

The control IDs are internal SIH26155 project control IDs.
Controls operate on vendor-neutral SBM semantic fields.

Vendor-specific configuration is normalized by the parser
before compliance evaluation.
"""


CIS_CONTROLS = {
    "MGMT-SSH-001": {
        "control_id": "MGMT-SSH-001",
        "framework": "CIS",
        "title": "SSH must use SSHv2",
        "semantic_field": "management.ssh.version",
        "description": "SSH management access must use SSH version 2.",
        "expected": 2,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },

    "MGMT-TELNET-001": {
        "control_id": "MGMT-TELNET-001",
        "framework": "CIS",
        "title": "Telnet management must be disabled",
        "semantic_field": "management.telnet.enabled",
        "description": "Telnet management access must be disabled.",
        "expected": False,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },

    "MGMT-HTTP-001": {
        "control_id": "MGMT-HTTP-001",
        "framework": "CIS",
        "title": "HTTP management must be disabled",
        "semantic_field": "management.http.enabled",
        "description": "HTTP management access must be disabled.",
        "expected": False,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },

    "AUTH-LOGIN-001": {
        "control_id": "AUTH-LOGIN-001",
        "framework": "CIS",
        "title": "Login protection must be configured",
        "semantic_field": "authentication.login_protection.enabled",
        "description": "Login protection must be configured.",
        "expected": True,
        "operator": "eq",
        "severity": "medium",
        "evidence_required": True,
        "remediation_required": True,
    },

    "LOG-001": {
        "control_id": "LOG-001",
        "framework": "CIS",
        "title": "Security logging must be enabled",
        "semantic_field": "logging.enabled",
        "description": "Security logging must be enabled.",
        "expected": True,
        "operator": "eq",
        "severity": "medium",
        "evidence_required": True,
        "remediation_required": True,
    },
}


def get_cis_control(control_id: str):
    """Return a CIS control by internal project control ID."""
    return CIS_CONTROLS.get(control_id)


def get_all_cis_controls():
    """Return all CIS controls."""
    return list(CIS_CONTROLS.values())