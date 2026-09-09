from sih26155.compliance.evaluator.engine import ComplianceEvaluator
from sih26155.compliance.policy.models import PolicyRule, PolicySet
from sih26155.core.schema.models import SecurityBaseline


def make_policy() -> PolicySet:
    return PolicySet(
        name="test-policy",
        rules=[
            PolicyRule(
                control_id="MGMT-SSH-001",
                semantic_field="management.ssh.version",
                description="SSH must use version 2.",
                operator="eq",
                expected=2,
                severity="high",
            )
        ],
    )


def test_compliance_pass():
    sbm = SecurityBaseline()
    sbm.management.ssh.version = 2

    findings = ComplianceEvaluator().evaluate(
        sbm=sbm,
        policy=make_policy(),
    )

    assert len(findings) == 1
    assert findings[0].status == "PASS"
    assert findings[0].observed == 2


def test_compliance_fail():
    sbm = SecurityBaseline()
    sbm.management.ssh.version = 1

    findings = ComplianceEvaluator().evaluate(
        sbm=sbm,
        policy=make_policy(),
    )

    assert len(findings) == 1
    assert findings[0].status == "FAIL"
    assert findings[0].observed == 1


def test_compliance_unknown_when_value_missing():
    sbm = SecurityBaseline()

    findings = ComplianceEvaluator().evaluate(
        sbm=sbm,
        policy=make_policy(),
    )

    assert len(findings) == 1
    assert findings[0].status == "UNKNOWN"
    assert findings[0].observed is None