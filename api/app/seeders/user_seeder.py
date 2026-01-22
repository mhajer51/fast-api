from app.db.session import SessionLocal
from app.repositories import user_repository
from app.schemas.user import UserCreate
from app.seeders.base import Seeder


class UserSeeder(Seeder):
    def run(self) -> None:
        with SessionLocal() as db:
            existing = user_repository.get_by_email(db, "admin@example.com")
            if existing:
                return
            user_repository.create_user(
                db,
                UserCreate(
                    name="Admin",
                    email="admin@example.com",
                    username="admin",
                    password="ChangeMe123!",
                ),
            )
