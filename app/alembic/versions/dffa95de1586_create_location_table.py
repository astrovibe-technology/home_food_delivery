"""create location_table

Revision ID: dffa95de1586
Revises: ea210679da80
Create Date: 2026-02-14 12:58:31.388810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dffa95de1586'
down_revision: Union[str, Sequence[str], None] = 'ea210679da80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
