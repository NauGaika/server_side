"""empty message

Revision ID: cbb6e0bad077
Revises: 5ee8f5972bb0
Create Date: 2018-10-16 19:03:08.666060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbb6e0bad077'
down_revision = '5ee8f5972bb0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('good', sa.Column('price', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('good', 'price')
    # ### end Alembic commands ###
