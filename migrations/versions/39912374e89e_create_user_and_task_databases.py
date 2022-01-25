"""Create user and task databases

Revision ID: 39912374e89e
Revises: 
Create Date: 2022-01-25 22:22:47.222309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39912374e89e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.BINARY(length=16), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('task',
    sa.Column('id', sa.BINARY(length=16), nullable=False),
    sa.Column('owner_id', sa.BINARY(length=16), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.Column('saved_timezone', sa.String(length=100), nullable=True),
    sa.Column('favorite', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###