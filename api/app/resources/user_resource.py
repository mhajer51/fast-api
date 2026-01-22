from app.models.user import User
from app.schemas.user import UserOut


class UserResource:
    @staticmethod
    def from_model(user: User) -> UserOut:
        return UserOut.model_validate(user)

    @staticmethod
    def list(users: list[User]) -> list[UserOut]:
        return [UserOut.model_validate(user) for user in users]
