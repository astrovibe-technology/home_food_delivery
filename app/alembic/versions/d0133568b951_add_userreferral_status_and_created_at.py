"""add userreferral status and created_at

Revision ID: d0133568b951
Revises: 9f81d7602dcd
Create Date: 2026-02-01 11:20:51.505504

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0133568b951'
down_revision: Union[str, Sequence[str], None] = '9f81d7602dcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
