"""
Vendor-neutral STIG compliance control catalogue.

These controls operate on normalized SBM semantic fields.
Vendor-specific configuration parsing is handled by the
parser and normalization layer.

Vendor-specific remediation is maintained separately from
the compliance control definitions.
"""


STIG_CONTROLS = {
    "SSH-001": {
        "control_id": "SSH-001",
        "title": "SSH must use SSHv2",
        "semantic_field": "management.ssh.version",
        "description": "SSH management access must use SSH version 2.",
        "category": "Network Access",
        "severity": "high",
    },

    "MGMT-001": {
        "control_id": "MGMT-001",
        "title": "Telnet must be disabled",
        "semantic_field": "management.telnet.enabled",
        "description": "Telnet management access must be disabled.",
        "category": "Network Access",
        "severity": "high",
    },

    "MGMT-002": {
        "control_id": "MGMT-002",
        "title": "HTTP management must be disabled",
        "semantic_field": "management.http.enabled",
        "description": "HTTP management access must be disabled.",
        "category": "Network Access",
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


def get_stig_control(control_id: str):
    """
    Return a STIG control by its project control ID.

    Args:
        control_id: Project-level control identifier.

    Returns:
        Control dictionary if found, otherwise None.
    """
    return STIG_CONTROLS.get(control_id)


def get_all_stig_controls():
    """
    Return all STIG controls.

    Returns:
        List of STIG control definitions.
    """
    return list(STIG_CONTROLS.values())