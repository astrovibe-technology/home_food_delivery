"""add referral restaurant user_setting wallet wallet_transaction

Revision ID: 210683a054fa
Revises: xxxxxxxxxxxx
Create Date: 2026-01-24 12:12:22.329539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '210683a054fa'
down_revision: Union[str, Sequence[str], None] = 'xxxxxxxxxxxx'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
