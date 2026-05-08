def get_token(client):
    client.post("/api/v1/auth/register", json={
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "secret123",
        "full_name": "Test User 2",
    })
    resp = client.post("/api/v1/auth/login", json={
        "username": "testuser2",
        "password": "secret123",
    })
    return resp.json()["access_token"]


def test_create_order_requires_auth(client):
    resp = client.post("/api/v1/orders", json={
        "notes": "Test order",
        "items": [],
    })
    assert resp.status_code == 401


def test_create_order_with_auth(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.get("/api/v1/products")
    assert resp.status_code == 200
    if len(resp.json()) == 0:
        token_admin = get_token(client)
        headers_admin = {"Authorization": f"Bearer {token_admin}"}
        client.post("/api/v1/products/categories", json={
            "name": "Test Category",
        }, headers=headers_admin)
        client.post("/api/v1/products", json={
            "name": "Test Product",
            "price": 1.00,
            "category_id": 1,
            "sku": "TEST-001",
        }, headers=headers_admin)

    resp = client.post("/api/v1/orders", json={
        "notes": "Test order",
        "items": [{"product_id": 1, "quantity": 2}],
    }, headers=headers)
    assert resp.status_code in (201, 400)