"""create timings table

Revision ID: 5e4d1ac913be
Revises: a97ee3ce7fc2
Create Date: 2026-02-02 15:10:06.097458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e4d1ac913be'
down_revision: Union[str, Sequence[str], None] = 'a97ee3ce7fc2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
