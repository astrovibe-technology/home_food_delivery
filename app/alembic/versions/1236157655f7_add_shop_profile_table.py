"""add shop profile table

Revision ID: 1236157655f7
Revises: 72e0e03f2f08
Create Date: 2026-01-31 09:30:10.434081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1236157655f7'
down_revision: Union[str, Sequence[str], None] = '72e0e03f2f08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
