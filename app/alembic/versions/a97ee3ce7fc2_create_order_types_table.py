"""create order_types table

Revision ID: a97ee3ce7fc2
Revises: 1e2464f3286d
Create Date: 2026-02-02 13:49:25.604004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a97ee3ce7fc2'
down_revision: Union[str, Sequence[str], None] = '1e2464f3286d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
