"""
Vendor-neutral CIS compliance control catalogue.

These controls operate on normalized SBM semantic fields.
Vendor-specific configuration parsing is handled by the
parser and normalization layer.

The same control can therefore be evaluated for multiple
vendors such as Cisco, Juniper, and Palo Alto, provided that
their parsers normalize the relevant configuration into the
same SBM semantic field.
"""


CIS_CONTROLS = {
    "SSH-001": {
        "control_id": "SSH-001",
        "title": "SSH must use SSHv2",
        "semantic_field": "management.ssh.version",
        "description": "SSH management access must use SSH version 2.",
        "category": "SSH",
        "severity": "high",
    },

    "MGMT-001": {
        "control_id": "MGMT-001",
        "title": "Telnet must be disabled",
        "semantic_field": "management.telnet.enabled",
        "description": "Telnet management access must be disabled.",
        "category": "Management",
        "severity": "high",
    },

    "MGMT-002": {
        "control_id": "MGMT-002",
        "title": "HTTP management must be disabled",
        "semantic_field": "management.http.enabled",
        "description": "HTTP management access must be disabled.",
        "category": "Management",
        "severity": "high",
    },

    "AUTH-001": {
        "control_id": "AUTH-001",
        "title": "Login protection must be configured",
        "semantic_field": "authentication.login_protection.enabled",
        "description": "Login protection must be configured.",
        "category": "Authentication",
        "severity": "medium",
    },

    "LOG-001": {
        "control_id": "LOG-001",
        "title": "Security logging must be enabled",
        "semantic_field": "logging.security.enabled",
        "description": "Security logging must be enabled.",
        "category": "Logging",
        "severity": "medium",
    },
}


def get_cis_control(control_id: str):
    """
    Return a CIS control by its control ID.

    Args:
        control_id: Unique CIS control identifier.

    Returns:
        The control dictionary if found, otherwise None.
    """
    return CIS_CONTROLS.get(control_id)


def get_all_cis_controls():
    """
    Return all CIS controls.

    Returns:
        A list containing all CIS control definitions.
    """
    return list(CIS_CONTROLS.values())