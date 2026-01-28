"""add restaurant timing fields

Revision ID: f59ebf137681
Revises: 210683a054fa
Create Date: 2026-01-26 18:09:49.217845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f59ebf137681'
down_revision: Union[str, Sequence[str], None] = '210683a054fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
