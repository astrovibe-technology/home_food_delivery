"""empty message

Revision ID: 5102cee9b2bc
Revises: f59ebf137681
Create Date: 2026-01-28 13:00:52.681439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5102cee9b2bc'
down_revision: Union[str, Sequence[str], None] = 'f59ebf137681'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
