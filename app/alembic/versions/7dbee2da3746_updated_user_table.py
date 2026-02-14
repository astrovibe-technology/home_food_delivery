"""updated user_table

Revision ID: 7dbee2da3746
Revises: dffa95de1586
Create Date: 2026-02-14 13:21:54.201527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dbee2da3746'
down_revision: Union[str, Sequence[str], None] = 'dffa95de1586'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
