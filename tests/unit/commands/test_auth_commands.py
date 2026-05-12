import pytest
from unittest.mock import Mock
from app.application.commands.auth_commands import RegisterUserCommand, LoginCommand
from app.application.dtos.auth_dtos import UserCreateDTO, LoginRequestDTO
from app.domain.entities.user import User, UserRole
from app.infrastructure.auth.password_handler import hash_password


class TestRegisterUserCommand:
    def test_register_user_success(self):
        mock_repo = Mock()
        mock_repo.get_by_username.return_value = None
        mock_repo.get_by_email.return_value = None
        mock_repo.create.return_value = User(
            id=1,
            username="testuser",
            email="test@test.com",
            hashed_password="hashed",
            full_name="Test User",
            role=UserRole.WAREHOUSE,
        )

        command = RegisterUserCommand(mock_repo)
        dto = UserCreateDTO(
            username="testuser",
            email="test@test.com",
            password="password123",
            full_name="Test User",
        )
        result = command.execute(dto)

        assert result.username == "testuser"
        mock_repo.create.assert_called_once()

    def test_register_duplicate_username(self):
        mock_repo = Mock()
        mock_repo.get_by_username.return_value = User(username="existing")

        command = RegisterUserCommand(mock_repo)
        dto = UserCreateDTO(
            username="existing",
            email="new@test.com",
            password="password123",
            full_name="Test",
        )

        with pytest.raises(ValueError, match="Username already exists"):
            command.execute(dto)

    def test_register_duplicate_email(self):
        mock_repo = Mock()
        mock_repo.get_by_username.return_value = None
        mock_repo.get_by_email.return_value = User(email="existing@test.com")

        command = RegisterUserCommand(mock_repo)
        dto = UserCreateDTO(
            username="newuser",
            email="existing@test.com",
            password="password123",
            full_name="Test",
        )

        with pytest.raises(ValueError, match="Email already exists"):
            command.execute(dto)


class TestLoginCommand:
    @pytest.fixture
    def valid_password(self):
        return "testpassword123"

    @pytest.fixture
    def valid_hash(self, valid_password):
        return hash_password(valid_password)

    def test_login_success(self, valid_password, valid_hash):
        mock_repo = Mock()
        mock_repo.get_by_username.return_value = User(
            id=1,
            username="testuser",
            hashed_password=valid_hash,
            is_active=True,
            role=UserRole.WAREHOUSE,
        )

        command = LoginCommand(mock_repo)
        dto = LoginRequestDTO(username="testuser", password=valid_password)
        result = command.execute(dto)

        assert hasattr(result, "access_token")
        assert result.access_token is not None

    def test_login_invalid_username(self):
        mock_repo = Mock()
        mock_repo.get_by_username.return_value = None

        command = LoginCommand(mock_repo)
        dto = LoginRequestDTO(username="nonexistent", password="password123")

        with pytest.raises(ValueError, match="Invalid credentials"):
            command.execute(dto)

    def test_login_invalid_password(self, valid_hash):
        mock_repo = Mock()
        mock_repo.get_by_username.return_value = User(
            id=1,
            username="testuser",
            hashed_password=valid_hash,
            is_active=True,
        )

        command = LoginCommand(mock_repo)
        dto = LoginRequestDTO(username="testuser", password="wrongpassword")

        with pytest.raises(ValueError, match="Invalid credentials"):
            command.execute(dto)

    def test_login_inactive_user(self, valid_hash):
        mock_repo = Mock()
        mock_repo.get_by_username.return_value = User(
            id=1,
            username="testuser",
            hashed_password=valid_hash,
            is_active=False,
        )

        command = LoginCommand(mock_repo)
        dto = LoginRequestDTO(username="testuser", password="testpassword123")

        with pytest.raises(ValueError, match="User is inactive"):
            command.execute(dto)
