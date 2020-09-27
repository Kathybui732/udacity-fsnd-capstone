"""empty message

Revision ID: af4e8d208a73
Revises: 
Create Date: 2020-09-26 18:38:24.208211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af4e8d208a73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('state', sa.String(length=80), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lng', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('state')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('roadtrips',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('start_city_id', sa.Integer(), nullable=False),
    sa.Column('end_city_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['end_city_id'], ['cities.id'], ),
    sa.ForeignKeyConstraint(['start_city_id'], ['cities.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roadtrips')
    op.drop_table('users')
    op.drop_table('cities')
    # ### end Alembic commands ###
