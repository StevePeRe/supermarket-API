def test_register_and_login(client):
    resp = client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "secret123",
        "full_name": "Test User",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "testuser"
    assert data["role"] == "warehouse"

    resp = client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "secret123",
    })
    assert resp.status_code == 200
    token = resp.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"


def test_register_duplicate(client):
    payload = {
        "username": "dup",
        "email": "dup@example.com",
        "password": "pass",
        "full_name": "Dup",
    }
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 201
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


def test_login_invalid(client):
    resp = client.post("/api/v1/auth/login", json={
        "username": "nobody",
        "password": "wrong",
    })
    assert resp.status_code == 401
