"""empty message

Revision ID: 5ee8f5972bb0
Revises: 0e5120bf7d90
Create Date: 2018-10-16 12:24:54.460257

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5ee8f5972bb0'
down_revision = '0e5120bf7d90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('good', 'is_calculated')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('good', sa.Column('is_calculated', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
