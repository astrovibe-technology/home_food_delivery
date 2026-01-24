"""add remaining core tables

Revision ID: xxxxxxxxxxxx
Revises: 649172e84633
Create Date: 2026-01-23
"""

from alembic import op
import sqlalchemy as sa


revision = 'xxxxxxxxxxxx'
down_revision = '649172e84633'
branch_labels = None
depends_on = None


def upgrade():
    # ---------- ADDRESS ----------
    op.create_table(
        'addresses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('type', sa.String),
        sa.Column('address', sa.String),
        sa.Column('latitude', sa.String),
        sa.Column('longitude', sa.String),
    )

    # ---------- CART ----------
    op.create_table(
        'carts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
    )

    # ---------- CART ITEMS ----------
    op.create_table(
        'cart_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('cart_id', sa.Integer, sa.ForeignKey('carts.id')),
        sa.Column('menu_id', sa.Integer, sa.ForeignKey('menus.id')),
        sa.Column('quantity', sa.Integer, default=1),
    )

    # ---------- MENU ----------
    op.create_table(
        'menus',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('restaurant_id', sa.Integer, sa.ForeignKey('restaurants.id')),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('price', sa.Integer),
        sa.Column('is_available', sa.Boolean, default=True),
    )

    # ---------- COOKING STATUS ----------
    op.create_table(
        'cooking_status',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('orders.id')),
        sa.Column('status', sa.String),
    )

    # ---------- ORDER ----------
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('total_amount', sa.Integer),
        sa.Column('status', sa.String),
        sa.Column('created_at', sa.DateTime),
    )

    # ---------- ORDER ITEMS ----------
    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('orders.id')),
        sa.Column('menu_id', sa.Integer, sa.ForeignKey('menus.id')),
        sa.Column('quantity', sa.Integer),
        sa.Column('price', sa.Integer),
    )

    # ---------- POOLING ORDER ----------
    op.create_table(
        'pooling_orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('orders.id')),
        sa.Column('group_id', sa.String),
    )

    # ---------- FAQ ----------
    op.create_table(
        'faq',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('question', sa.String),
        sa.Column('answer', sa.String),
    )

    # ---------- INCENTIVE ----------
    op.create_table(
        'incentives',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('amount', sa.Integer),
        sa.Column('reason', sa.String),
    )


def downgrade():
    op.drop_table('incentives')
    op.drop_table('faq')
    op.drop_table('pooling_orders')
    op.drop_table('order_items')
    op.drop_table('orders')
    op.drop_table('cooking_status')
    op.drop_table('menus')
    op.drop_table('cart_items')
    op.drop_table('carts')
    op.drop_table('addresses')