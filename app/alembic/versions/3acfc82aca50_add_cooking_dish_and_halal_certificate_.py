"""add cooking dish and halal certificate fields

Revision ID: 3acfc82aca50
Revises: 1236157655f7
Create Date: 2026-01-31 10:30:45.154778

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3acfc82aca50'
down_revision: Union[str, Sequence[str], None] = '1236157655f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
