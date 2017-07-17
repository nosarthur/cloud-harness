"""empty message

Revision ID: d3144d5d2f80
Revises: 03e84b7369b8
Create Date: 2017-07-17 07:39:55.186581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3144d5d2f80'
down_revision = '03e84b7369b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('workers', 'price',
               existing_type=sa.NUMERIC(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('workers', 'price',
               existing_type=sa.NUMERIC(),
               nullable=False)
    # ### end Alembic commands ###
