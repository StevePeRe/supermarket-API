from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class GetUserByIdQuery:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int) -> User | None:
        return self.user_repo.get_by_id(user_id)