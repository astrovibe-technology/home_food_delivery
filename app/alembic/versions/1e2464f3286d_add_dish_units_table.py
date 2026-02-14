"""add dish_units table

Revision ID: 1e2464f3286d
Revises: d0133568b951
Create Date: 2026-02-02 13:24:53.205043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e2464f3286d'
down_revision: Union[str, Sequence[str], None] = 'd0133568b951'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
