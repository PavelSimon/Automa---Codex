from uuid import uuid4

from fastapi.testclient import TestClient

from automa.api.app import app
from automa.core.db import get_session
from automa.domain.models import User
from sqlmodel import select


def get_token(client: TestClient) -> str:
    r = client.post(
        "/api/v1/auth/token",
        data={"username": "admin@example.com", "password": "admin"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_auth_and_me():
    client = TestClient(app)
    token = get_token(client)
    r = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "admin@example.com"
    assert data["is_admin"] is True


def test_create_and_list_agents():
    client = TestClient(app)
    token = get_token(client)

    # create
    payload = {"name": "agent-alpha", "description": "test agent"}
    r = client.post("/api/v1/agents", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    created = r.json()
    assert created["name"] == "agent-alpha"

    # list
    r = client.get("/api/v1/agents")
    assert r.status_code == 200
    names = [a["name"] for a in r.json()]
    assert "agent-alpha" in names


def test_ui_register_sets_cookie_and_refresh_header():
    client = TestClient(app)
    email = f"user-{uuid4().hex}@example.com"

    r = client.post(
        "/ui/auth/register",
        data={"email": email, "password": "mypass123", "full_name": "Test User"},
    )
    assert r.status_code == 200
    assert r.headers.get("HX-Refresh") == "true"
    assert r.headers.get("HX-Redirect") == "/"
    assert client.cookies.get("automa_access_token")

    with get_session() as session:
        user = session.exec(select(User).where(User.email == email)).first()
        assert user is not None
