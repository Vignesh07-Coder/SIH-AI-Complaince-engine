"""
DISA STIG compliance control catalogue.

Target:
    Cisco IOS XE Router NDM STIG

The control IDs are internal SIH26155 project control IDs.
The STIG reference identifies the applicable STIG requirement.

STIG requirements are platform-specific. Vendor and platform
information must come from the parser/device context.
"""


STIG_CONTROLS = {
    "MGMT-SSH-001": {
        "control_id": "MGMT-SSH-001",
        "framework": "STIG",
        "stig_reference": "CISC-ND-001210",
        "finding_id": "V-215845",
        "benchmark": "Cisco IOS XE Router NDM STIG",
        "title": "Protect remote maintenance sessions",
        "semantic_field": "management.ssh.version",
        "description": (
            "Remote maintenance sessions must use approved "
            "cryptographic mechanisms."
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
        "stig_reference": "CISC-ND-001210",
        "finding_id": "V-215845",
        "benchmark": "Cisco IOS XE Router NDM STIG",
        "title": "Use secure protocols for remote maintenance",
        "semantic_field": "management.telnet.enabled",
        "description": (
            "Unsecured remote-management protocols such as Telnet "
            "must not be used where secure alternatives are required."
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
        "stig_reference": "CISC-ND-001210",
        "finding_id": "V-215845",
        "benchmark": "Cisco IOS XE Router NDM STIG",
        "title": "Protect remote maintenance sessions",
        "semantic_field": "management.http.enabled",
        "description": (
            "Unsecured HTTP management must not be used where "
            "cryptographically protected management is required."
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
        "stig_reference": "CISC-ND-001370",
        "finding_id": "V-215854",
        "benchmark": "Cisco IOS XE Router NDM STIG",
        "title": "Use authentication servers for administrative access",
        "semantic_field": "authentication.login_protection.enabled",
        "description": (
            "Administrative access must use approved authentication "
            "mechanisms before access is granted."
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
        "stig_reference": "CISC-ND-001450",
        "finding_id": "V-220139",
        "benchmark": "Cisco IOS XE Router NDM STIG",
        "title": "Forward log data to multiple syslog servers",
        "semantic_field": "logging.enabled",
        "description": (
            "The Cisco device must be configured to forward "
            "security and administrative log data."
        ),
        "expected": True,
        "operator": "eq",
        "severity": "high",
        "evidence_required": True,
        "remediation_required": True,
    },
}


def get_stig_control(control_id: str):
    """Return a STIG control by internal project control ID."""
    return STIG_CONTROLS.get(control_id)


def get_all_stig_controls():
    """Return all STIG controls."""
    return list(STIG_CONTROLS.values())