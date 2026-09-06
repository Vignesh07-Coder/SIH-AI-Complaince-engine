"""
Vendor-neutral NIST compliance control catalogue.

These controls operate on normalized SBM semantic fields.
Vendor-specific configuration parsing is handled by the
parser and normalization layer.

The same normalized security facts can be evaluated across
different network vendors.
"""


NIST_CONTROLS = {
    "SSH-001": {
        "control_id": "SSH-001",
        "title": "SSH must use SSHv2",
        "semantic_field": "management.ssh.version",
        "description": "SSH management access must use SSH version 2.",
        "category": "Access Control",
        "severity": "high",
    },

    "MGMT-001": {
        "control_id": "MGMT-001",
        "title": "Telnet must be disabled",
        "semantic_field": "management.telnet.enabled",
        "description": "Telnet management access must be disabled.",
        "category": "Access Control",
        "severity": "high",
    },

    "MGMT-002": {
        "control_id": "MGMT-002",
        "title": "HTTP management must be disabled",
        "semantic_field": "management.http.enabled",
        "description": "HTTP management access must be disabled.",
        "category": "Access Control",
        "severity": "high",
    },

    "AUTH-001": {
        "control_id": "AUTH-001",
        "title": "Login protection must be configured",
        "semantic_field": "authentication.login_protection.enabled",
        "description": "Login protection must be configured.",
        "category": "Identification and Authentication",
        "severity": "medium",
    },

    "LOG-001": {
        "control_id": "LOG-001",
        "title": "Security logging must be enabled",
        "semantic_field": "logging.security.enabled",
        "description": "Security logging must be enabled.",
        "category": "Audit and Accountability",
        "severity": "medium",
    },
}


def get_nist_control(control_id: str):
    """
    Return a NIST control by its project control ID.

    Args:
        control_id: Project-level control identifier.

    Returns:
        Control dictionary if found, otherwise None.
    """
    return NIST_CONTROLS.get(control_id)


def get_all_nist_controls():
    """
    Return all NIST controls.

    Returns:
        List of NIST control definitions.
    """
    return list(NIST_CONTROLS.values())