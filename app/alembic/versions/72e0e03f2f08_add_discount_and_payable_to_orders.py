"""add discount and payable to orders

Revision ID: 72e0e03f2f08
Revises: 338fe0dca766
Create Date: 2026-01-28 13:25:05.990012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72e0e03f2f08'
down_revision: Union[str, Sequence[str], None] = '338fe0dca766'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
