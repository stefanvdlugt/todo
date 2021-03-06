"""Add settings table

Revision ID: 765ee637465c
Revises: 1f1421200142
Create Date: 2022-03-29 13:38:16.154735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '765ee637465c'
down_revision = '1f1421200142'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('global_setting',
    sa.Column('key', sa.String(length=32), nullable=False),
    sa.Column('value', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('key')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('global_setting')
    # ### end Alembic commands ###
