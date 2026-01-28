"""add promo code table

Revision ID: 338fe0dca766
Revises: 5102cee9b2bc
Create Date: 2026-01-28 13:18:01.559425
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '338fe0dca766'
down_revision: Union[str, Sequence[str], None] = '5102cee9b2bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'promo_codes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('code', sa.String(), nullable=False, unique=True),
        sa.Column('discount_type', sa.String(), nullable=False),  # FLAT / PERCENT
        sa.Column('discount_value', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.true())
    )


def downgrade() -> None:
    op.drop_table('promo_codes')