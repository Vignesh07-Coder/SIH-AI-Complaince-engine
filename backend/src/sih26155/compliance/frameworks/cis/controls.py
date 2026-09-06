"""
CIS compliance control catalogue.

Vendor-neutral SIH26155 controls mapped to CIS security
configuration principles.

Vendor-specific CIS Benchmarks are handled separately
through framework/platform mappings.
"""

CIS_CONTROLS = {
    "MGMT-SSH-001": {
        "control_id": "MGMT-SSH-001",
        "framework": "CIS",
        "title": "Use secure SSH management",
        "semantic_field": "management.ssh.version",
        "description": (
            "Management access must use SSH version 2."
        ),
        "expected": 2,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },

    "MGMT-TELNET-001": {
        "control_id": "MGMT-TELNET-001",
        "framework": "CIS",
        "title": "Disable Telnet management",
        "semantic_field": "management.telnet.enabled",
        "description": (
            "Telnet management access must be disabled."
        ),
        "expected": False,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },

    "MGMT-HTTP-001": {
        "control_id": "MGMT-HTTP-001",
        "framework": "CIS",
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
        "framework": "CIS",
        "title": "Enable login protection",
        "semantic_field": "authentication.login_protection.enabled",
        "description": (
            "Management login protection must be enabled."
        ),
        "expected": True,
        "operator": "eq",
        "severity": "medium",
        "evidence_required": True,
        "remediation_required": True,
    },

    "LOG-001": {
        "control_id": "LOG-001",
        "framework": "CIS",
        "title": "Enable security logging",
        "semantic_field": "logging.enabled",
        "description": (
            "Security logging must be enabled."
        ),
        "expected": True,
        "operator": "eq",
        "severity": "medium",
        "evidence_required": True,
        "remediation_required": True,
    },
}


def get_cis_control(control_id: str):
    return CIS_CONTROLS.get(control_id)


def get_all_cis_controls():
    return list(CIS_CONTROLS.values())
