"""initial migration rooms

Revision ID: 8fc1a940c8a7
Revises: 7f85d342381e
Create Date: 2025-10-03 10:16:18.148627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '8fc1a940c8a7'
down_revision: Union[str, Sequence[str], None] = '7f85d342381e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rooms',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('hotel_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=100), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('price', sa.Integer(), nullable=False),
                    sa.Column('quantity', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('rooms')
