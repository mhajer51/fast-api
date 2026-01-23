from pathlib import Path

from alembic import command
from alembic.config import Config


def _alembic_config() -> Config:
    api_root = Path(__file__).resolve().parents[2]
    config_path = api_root / "alembic.ini"
    config = Config(str(config_path))
    config.set_main_option("script_location", str(api_root / "alembic"))
    return config


def upgrade(revision: str = "head") -> None:
    command.upgrade(_alembic_config(), revision)
