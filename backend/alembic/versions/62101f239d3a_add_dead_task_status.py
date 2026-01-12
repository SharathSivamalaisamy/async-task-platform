"""add DEAD task status

Revision ID: 62101f239d3a
Revises: 63a32396273b
Create Date: 2026-01-11 08:37:01.565981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62101f239d3a'
down_revision: Union[str, None] = '63a32396273b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
