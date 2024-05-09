import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys

from pathlib import Path
parent_dir = Path(__file__).parents[1]
sys.path.append(str(parent_dir))
from main import app  # noqa: E402
from models.db import Base, get_db  # noqa: E402

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/products?charset=utf8mb4"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def login_for_access_token():
    response = client.post(
        "/login", data={"username": "testuser", "password": "Test@123"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def flush_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_signup(flush_db):
    response = client.post(
        "/signup",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Test@123",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "User created successfully"}


def test_login():
    token = login_for_access_token()
    assert token


def test_get_products():
    token = login_for_access_token()
    response = client.get("/products", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "products" in response.json()


def test_create_product():
    token = login_for_access_token()
    response = client.post(
        "/products",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Product 1",
            "description": "A product description",
            "price": 10.99,
            "count": 100,
        },
    )
    assert response.status_code == 200
    assert "Product Added" in response.json()


def test_get_product_by_id():
    token = login_for_access_token()
    response = client.get("/products/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "Product" in response.json()


def test_update_product():
    token = login_for_access_token()
    response = client.put(
        "/products/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Updated Product",
            "description": "An updated product",
            "price": 12.99,
            "count": 80,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"Product Updated": 1}


def test_delete_product():
    token = login_for_access_token()
    response = client.delete(
        "/products/1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"Product Deleted": 1}


def test_delete_all_products():
    token = login_for_access_token()
    response = client.delete("/products", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "All products deleted successfully"}