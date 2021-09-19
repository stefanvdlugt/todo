"""Create task table

Revision ID: 9053c5495a16
Revises: a8fca8820473
Create Date: 2021-09-19 22:04:35.373754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9053c5495a16'
down_revision = 'a8fca8820473'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.BINARY(length=16), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('deadline', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    # ### end Alembic commands ###
