from pathlib import Path

from fastapi.testclient import TestClient

from sih26155.api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analysis_endpoint_runs_full_pipeline():
    config_path = Path("data/configs/cisco/test.conf")

    config = config_path.read_text(encoding="utf-8")

    response = client.post(
        "/api/analysis",
        json={
            "config": config,
            "source_file": "test.conf",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["vendor"]["name"] == "cisco"

    assert "facts" in body
    assert "evidence" in body
    assert "baseline" in body
    assert "findings" in body
    assert "remediations" in body

    findings = {
        finding["control_id"]: finding
        for finding in body["findings"]
    }

    assert findings["MGMT-SSH-001"]["status"] == "PASS"
    assert findings["MGMT-TELNET-001"]["status"] == "PASS"
    assert findings["MGMT-HTTP-001"]["status"] == "FAIL"

    remediations = body["remediations"]

    assert len(remediations) == 1
    assert remediations[0]["control_id"] == "MGMT-HTTP-001"
    assert remediations[0]["command"] == "no ip http server"