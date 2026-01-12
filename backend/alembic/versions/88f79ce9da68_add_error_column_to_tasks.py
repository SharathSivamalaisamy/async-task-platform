"""add error column to tasks

Revision ID: 88f79ce9da68
Revises: a0713e09f6e0
Create Date: 2026-01-04 22:29:57.289161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88f79ce9da68'
down_revision: Union[str, None] = 'a0713e09f6e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "tasks",
        sa.Column("error", sa.Text(), nullable=True),
    )


def downgrade():
    op.drop_column("tasks", "error")