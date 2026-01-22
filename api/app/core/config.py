from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "local"

    MYSQL_HOST: str = "mariadb"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "app_db"
    MYSQL_USER: str = "app_user"
    MYSQL_PASSWORD: str = "app_pass"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""

    SMTP_HOST: str = "mailhog"
    SMTP_PORT: int = 1025

    @property
    def DATABASE_URL(self) -> str:
        # SQLAlchemy sync URL for MariaDB/MySQL via pymysql
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )

    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


settings = Settings()
