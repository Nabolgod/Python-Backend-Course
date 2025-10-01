"""initial migration

Revision ID: 7f85d342381e
Revises: 
Create Date: 2025-10-01 22:12:44.769369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '7f85d342381e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('hotels',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=100), nullable=False),
                    sa.Column('location', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('hotels')
