"""
CIS Controls v8.1 compliance control catalogue.

SIH26155 keeps its own stable internal control IDs and maps them
to official CIS Controls v8.1 Safeguards.

CIS Controls and CIS Benchmarks are different:
- CIS Controls v8.1 provide vendor-neutral Safeguards.
- CIS Benchmarks provide vendor/product-specific configuration guidance.

Vendor-specific Benchmark mappings are therefore kept separate.
"""

CIS_CONTROLS = {
    "MGMT-SSH-001": {
        "control_id": "MGMT-SSH-001",
        "framework": "CIS",
        "framework_version": "8.1",
        "framework_references": [
            {
                "framework": "CIS Controls",
                "version": "8.1",
                "identifier": "12.3",
                "title": "Securely Manage Network Infrastructure",
                "mapping_scope": "direct",
            },
            {
                "framework": "CIS Controls",
                "version": "8.1",
                "identifier": "12.6",
                "title": (
                    "Use of Secure Network Management and "
                    "Communication Protocols"
                ),
                "mapping_scope": "supporting",
            },
        ],
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
        "framework_version": "8.1",
        "framework_references": [
            {
                "framework": "CIS Controls",
                "version": "8.1",
                "identifier": "12.3",
                "title": "Securely Manage Network Infrastructure",
                "mapping_scope": "direct",
            },
            {
                "framework": "CIS Controls",
                "version": "8.1",
                "identifier": "12.6",
                "title": (
                    "Use of Secure Network Management and "
                    "Communication Protocols"
                ),
                "mapping_scope": "supporting",
            },
        ],
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
        "framework_version": "8.1",
        "framework_references": [
            {
                "framework": "CIS Controls",
                "version": "8.1",
                "identifier": "12.3",
                "title": "Securely Manage Network Infrastructure",
                "mapping_scope": "direct",
            },
            {
                "framework": "CIS Controls",
                "version": "8.1",
                "identifier": "12.6",
                "title": (
                    "Use of Secure Network Management and "
                    "Communication Protocols"
                ),
                "mapping_scope": "supporting",
            },
        ],
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
        "framework_version": "8.1",
        "framework_references": [
            {
                "framework": "CIS Controls",
                "version": "8.1",
                "identifier": "6.5",
                "title": "Require MFA for Administrative Access",
                "mapping_scope": "supporting",
            },
        ],
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
        "framework_version": "8.1",
        "framework_references": [
            {
                "framework": "CIS Controls",
                "version": "8.1",
                "identifier": "8.2",
                "title": "Collect Audit Logs",
                "mapping_scope": "direct",
            },
        ],
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
