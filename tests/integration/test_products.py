def get_token(client):
    client.post("/api/v1/auth/register", json={
        "username": "adminuser",
        "email": "admin@example.com",
        "password": "secret123",
        "full_name": "Admin User",
    })
    resp = client.post("/api/v1/auth/login", json={
        "username": "adminuser",
        "password": "secret123",
    })
    return resp.json()["access_token"]


def test_create_category_and_product(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post("/api/v1/products/categories", json={
        "name": "Dairy",
        "description": "Milk, cheese, yogurt",
    }, headers=headers)
    assert resp.status_code == 201
    cat = resp.json()
    assert cat["name"] == "Dairy"

    resp = client.post("/api/v1/products", json={
        "name": "Milk 1L",
        "price": 1.20,
        "category_id": cat["id"],
        "sku": "MLK-001",
    }, headers=headers)
    assert resp.status_code == 201
    prod = resp.json()
    assert prod["name"] == "Milk 1L"
    assert prod["sku"] == "MLK-001"

    resp = client.get("/api/v1/products")
    assert resp.status_code == 200
    assert len(resp.json()) == 1


def test_list_products_public(client):
    resp = client.get("/api/v1/products")
    assert resp.status_code == 200