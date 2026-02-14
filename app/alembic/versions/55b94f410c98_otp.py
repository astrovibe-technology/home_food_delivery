"""otp

Revision ID: 55b94f410c98
Revises: 5e4d1ac913be
Create Date: 2026-02-03 09:40:08.633213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55b94f410c98'
down_revision: Union[str, Sequence[str], None] = '5e4d1ac913be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
