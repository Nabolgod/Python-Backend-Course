"""add model users

Revision ID: 4a43a2e825b9
Revises: e37449779c51
Create Date: 2025-10-24 05:07:04.467723

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "4a43a2e825b9"
down_revision: Union[str, Sequence[str], None] = "e37449779c51"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("nick_name", sa.String(length=100), nullable=False),
        sa.Column("number", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
