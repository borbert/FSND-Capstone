"""empty message

Revision ID: 3af1fcd5c0f6
Revises: ac02c374f59e
Create Date: 2021-03-19 14:08:02.065288

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3af1fcd5c0f6'
down_revision = 'ac02c374f59e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=True),
    sa.Column('password', sa.String(length=250), nullable=True),
    sa.Column('firstname', sa.String(length=100), nullable=True),
    sa.Column('lastname', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('token', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('lists',
    sa.Column('list_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('list_name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date_added', sa.DateTime(), nullable=False),
    sa.Column('date_completed', sa.DateTime(), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('list_id')
    )
    op.drop_table('store')
    op.drop_table('list')
    op.add_column('item', sa.Column('item_id', sa.Integer(), nullable=False))
    op.drop_column('item', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('item', 'item_id')
    op.create_table('list',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('prod_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('store_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date_added', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('date_completed', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('complete', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['prod_id'], ['item.id'], name='list_prod_id_fkey'),
    sa.ForeignKeyConstraint(['store_id'], ['store.id'], name='list_store_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='list_pkey')
    )
    op.create_table('store',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('website', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('api', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('favorite', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='store_pkey')
    )
    op.drop_table('lists')
    op.drop_table('users')
    # ### end Alembic commands ###
