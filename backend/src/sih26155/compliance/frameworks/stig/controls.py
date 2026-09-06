"""
STIG compliance control catalogue.

Vendor-neutral SIH26155 controls mapped to STIG security
requirements.

Vendor-specific STIG implementation details are handled
outside this vendor-neutral catalogue.
"""

STIG_CONTROLS = {
    "MGMT-SSH-001": {
        "control_id": "MGMT-SSH-001",
        "framework": "STIG",
        "title": "Secure SSH management",
        "semantic_field": "management.ssh.version",
        "description": (
            "Remote management sessions must use approved "
            "secure mechanisms."
        ),
        "expected": 2,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },

    "MGMT-TELNET-001": {
        "control_id": "MGMT-TELNET-001",
        "framework": "STIG",
        "title": "Disable Telnet management",
        "semantic_field": "management.telnet.enabled",
        "description": (
            "Insecure Telnet management access must be disabled."
        ),
        "expected": False,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },

    "MGMT-HTTP-001": {
        "control_id": "MGMT-HTTP-001",
        "framework": "STIG",
        "title": "Disable insecure HTTP management",
        "semantic_field": "management.http.enabled",
        "description": (
            "Insecure HTTP management access must be disabled."
        ),
        "expected": False,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },

    "AUTH-LOGIN-001": {
        "control_id": "AUTH-LOGIN-001",
        "framework": "STIG",
        "title": "Protect management authentication",
        "semantic_field": "authentication.login_protection.enabled",
        "description": (
            "Management login access must use appropriate "
            "authentication protection."
        ),
        "expected": True,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },

    "LOG-001": {
        "control_id": "LOG-001",
        "framework": "STIG",
        "title": "Enable security logging",
        "semantic_field": "logging.enabled",
        "description": (
            "Security-relevant events must be logged."
        ),
        "expected": True,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },
}


def get_stig_control(control_id: str):
    return STIG_CONTROLS.get(control_id)


def get_all_stig_controls():
    return list(STIG_CONTROLS.values())
