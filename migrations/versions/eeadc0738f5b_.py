"""empty message

Revision ID: eeadc0738f5b
Revises: e5b730a0e84e
Create Date: 2018-10-16 10:54:58.604236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeadc0738f5b'
down_revision = 'e5b730a0e84e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('glass', sa.Column('formula_name', sa.String(length=240), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('glass', 'formula_name')
    # ### end Alembic commands ###
