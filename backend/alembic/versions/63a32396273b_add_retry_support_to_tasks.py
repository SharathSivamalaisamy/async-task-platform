"""add retry support to tasks

Revision ID: 63a32396273b
Revises: 8fc41f03b551
Create Date: 2026-01-08 17:03:54.674946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63a32396273b'
down_revision: Union[str, None] = '8fc41f03b551'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("tasks", sa.Column("retry_count", sa.Integer(), server_default="0", nullable=False))
    op.add_column("tasks", sa.Column("max_retries", sa.Integer(), server_default="3", nullable=False))


def downgrade():
    op.drop_column("tasks", "retry_count")
    op.drop_column("tasks", "max_retries")
