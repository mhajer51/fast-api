"""add username and password hash to users

Revision ID: 0002
Revises: 0001
Create Date: 2026-01-22
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("username", sa.String(length=80), nullable=True))
    op.add_column("users", sa.Column("password_hash", sa.String(length=255), nullable=True))
    op.create_index("ix_users_username", "users", ["username"], unique=True)


def downgrade():
    op.drop_index("ix_users_username", table_name="users")
    op.drop_column("users", "password_hash")
    op.drop_column("users", "username")
