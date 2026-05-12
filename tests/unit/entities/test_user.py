import pytest
from app.domain.entities.user import User, UserRole


class TestUserEntity:
    def test_user_creation_with_defaults(self):
        user = User(
            username="testuser",
            email="test@test.com",
            hashed_password="hash123",
            full_name="Test User",
        )

        assert user.username == "testuser"
        assert user.role == UserRole.WAREHOUSE
        assert user.is_active is True

    def test_user_creation_with_custom_role(self):
        user = User(
            username="admin",
            email="admin@test.com",
            hashed_password="hash123",
            full_name="Admin User",
            role=UserRole.ADMIN,
        )

        assert user.role == UserRole.ADMIN

    def test_user_to_dict_excludes_password(self):
        user = User(
            id=1,
            username="testuser",
            email="test@test.com",
            hashed_password="secret_hash",
            full_name="Test User",
            role=UserRole.ADMIN,
            is_active=True,
        )

        result = user.to_dict()

        assert result["id"] == 1
        assert result["username"] == "testuser"
        assert result["role"] == "admin"
        assert "hashed_password" not in result
        assert "password" not in result


class TestUserRole:
    def test_user_role_values(self):
        assert UserRole.ADMIN.value == "admin"
        assert UserRole.WAREHOUSE.value == "warehouse"
        assert UserRole.DELIVERY.value == "delivery"

    def test_user_role_is_string_enum(self):
        assert isinstance(UserRole.ADMIN, str)
        assert UserRole.ADMIN == "admin"
