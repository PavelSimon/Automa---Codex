from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from automa.api.app import app


def get_token(client: TestClient) -> str:
    r = client.post(
        "/api/v1/auth/token",
        data={"username": "admin@example.com", "password": "admin"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_create_and_list_jobs():
    client = TestClient(app)
    token = get_token(client)

    when = datetime.utcnow() + timedelta(seconds=1)
    payload = {"when": when.isoformat() + "Z"}
    r = client.post("/api/v1/jobs", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    job_id = r.json()["id"]
    assert job_id is not None

    r = client.get("/api/v1/jobs")
    assert r.status_code == 200
    ids = [j["id"] for j in r.json()]
    assert job_id in ids


def test_execute_job_updates_status():
    client = TestClient(app)
    token = get_token(client)

    script_payload = {"name": "script-dummy", "path": "scripts/dummy.py"}
    r = client.post(
        "/api/v1/scripts",
        json=script_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200, r.text
    script_id = r.json()["id"]

    r = client.post(
        "/api/v1/jobs",
        json={"script_id": script_id},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200, r.text
    job_id = r.json()["id"]

    from automa.scheduler.manager import execute_job

    execute_job(job_id)

    r = client.get("/api/v1/jobs")
    assert r.status_code == 200
    job = next(j for j in r.json() if j["id"] == job_id)
    assert job["status"] == "succeeded"
    assert job["last_exit_code"] == 0
    assert job["last_error"] is None
    assert job["last_run_at"] is not None
