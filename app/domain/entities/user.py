import enum
from dataclasses import dataclass


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    WAREHOUSE = "warehouse"
    DELIVERY = "delivery"


@dataclass
class User:
    id: int | None = None
    username: str = ""
    email: str = ""
    hashed_password: str = ""
    full_name: str = ""
    role: UserRole = UserRole.WAREHOUSE
    is_active: bool = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role.value,
            "is_active": self.is_active,
        }