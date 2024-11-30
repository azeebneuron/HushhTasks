import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.main import app
from app.database import Base, get_db
from app.models import User, Order

# Create a test database in memory
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to the Users and Orders API" in response.json()["message"]

class TestUsers:
    def test_create_user(self):
        response = client.post(
            "/users/",
            json={"name": "Test User", "email": "test@example.com"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test User"
        assert data["email"] == "test@example.com"
        assert "id" in data

    def test_create_user_duplicate_email(self):
        # Create first user
        client.post(
            "/users/",
            json={"name": "Test User", "email": "test@example.com"}
        )
        # Try to create user with same email
        response = client.post(
            "/users/",
            json={"name": "Another User", "email": "test@example.com"}
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_read_user(self):
        # Create user first
        create_response = client.post(
            "/users/",
            json={"name": "Test User", "email": "test@example.com"}
        )
        user_id = create_response.json()["id"]

        # Read user
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test User"
        assert data["email"] == "test@example.com"

    def test_read_user_not_found(self):
        response = client.get("/users/999")
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_update_user(self):
        # Create user first
        create_response = client.post(
            "/users/",
            json={"name": "Test User", "email": "test@example.com"}
        )
        user_id = create_response.json()["id"]

        # Update user
        response = client.put(
            f"/users/{user_id}",
            json={"name": "Updated User", "email": "updated@example.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated User"
        assert data["email"] == "updated@example.com"

    def test_delete_user(self):
        # Create user first
        create_response = client.post(
            "/users/",
            json={"name": "Test User", "email": "test@example.com"}
        )
        user_id = create_response.json()["id"]

        # Delete user
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204

        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

class TestOrders:
    @pytest.fixture
    def user_id(self):
        response = client.post(
            "/users/",
            json={"name": "Test User", "email": "test@example.com"}
        )
        return response.json()["id"]

    def test_create_order(self, user_id):
        response = client.post(
            "/orders/",
            params={"user_id": user_id},
            json={"product_name": "Test Product", "quantity": 1}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["product_name"] == "Test Product"
        assert data["quantity"] == 1
        assert data["user_id"] == user_id

    def test_create_order_invalid_quantity(self, user_id):
        response = client.post(
            "/orders/",
            params={"user_id": user_id},
            json={"product_name": "Test Product", "quantity": 0}
        )
        assert response.status_code == 422  # Validation error

    def test_create_order_user_not_found(self):
        response = client.post(
            "/orders/",
            params={"user_id": 999},
            json={"product_name": "Test Product", "quantity": 1}
        )
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_read_order(self, user_id):
        # Create order first
        create_response = client.post(
            "/orders/",
            params={"user_id": user_id},
            json={"product_name": "Test Product", "quantity": 1}
        )
        order_id = create_response.json()["id"]

        # Read order
        response = client.get(f"/orders/{order_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["product_name"] == "Test Product"
        assert data["quantity"] == 1

    def test_update_order(self, user_id):
        # Create order first
        create_response = client.post(
            "/orders/",
            params={"user_id": user_id},
            json={"product_name": "Test Product", "quantity": 1}
        )
        order_id = create_response.json()["id"]

        # Update order
        response = client.put(
            f"/orders/{order_id}",
            json={"product_name": "Updated Product", "quantity": 2}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["product_name"] == "Updated Product"
        assert data["quantity"] == 2

    def test_delete_order(self, user_id):
        # Create order first
        create_response = client.post(
            "/orders/",
            params={"user_id": user_id},
            json={"product_name": "Test Product", "quantity": 1}
        )
        order_id = create_response.json()["id"]

        # Delete order
        response = client.delete(f"/orders/{order_id}")
        assert response.status_code == 204

        # Verify order is deleted
        get_response = client.get(f"/orders/{order_id}")
        assert get_response.status_code == 404