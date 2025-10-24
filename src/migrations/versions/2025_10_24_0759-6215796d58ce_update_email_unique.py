"""update_email_unique

Revision ID: 6215796d58ce
Revises: 4a43a2e825b9
Create Date: 2025-10-24 07:59:38.317262

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "6215796d58ce"
down_revision: Union[str, Sequence[str], None] = "4a43a2e825b9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
