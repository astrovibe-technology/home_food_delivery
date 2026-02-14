"""add referral status and created_at

Revision ID: 9f81d7602dcd
Revises: 3acfc82aca50
Create Date: 2026-02-01 11:09:09.107260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f81d7602dcd'
down_revision: Union[str, Sequence[str], None] = '3acfc82aca50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
