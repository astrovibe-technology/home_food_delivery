"""add created_by to menus

Revision ID: ea210679da80
Revises: 55b94f410c98
Create Date: 2026-02-11 11:10:27.637614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea210679da80'
down_revision: Union[str, Sequence[str], None] = '55b94f410c98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "menus",
        sa.Column("created_by", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        "fk_menu_user",
        "menus",
        "users",
        ["created_by"],
        ["id"]
    )

def downgrade():
    op.drop_constraint("fk_menu_user", "menus", type_="foreignkey")
    op.drop_column("menus", "created_by")
