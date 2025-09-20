from fastapi.testclient import TestClient
from automa.api.app import app


def run():
    client = TestClient(app)

    # health
    r = client.get("/api/v1/health")
    assert r.status_code == 200 and r.json().get("status") == "ok"

    # auth
    r = client.post(
        "/api/v1/auth/token",
        data={"username": "admin@example.com", "password": "admin"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]

    # users/me
    r = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200

    # agents CRUD
    payload = {"name": "agent-smoke", "description": "smoke"}
    r = client.post("/api/v1/agents", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    r = client.get("/api/v1/agents")
    assert r.status_code == 200 and any(a["name"] == "agent-smoke" for a in r.json())

    # jobs create/list
    r = client.post("/api/v1/jobs", json={}, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    job_id = r.json()["id"]
    r = client.get("/api/v1/jobs")
    assert r.status_code == 200 and any(j["id"] == job_id for j in r.json())


if __name__ == "__main__":
    run()
    print("SMOKE TEST OK")
