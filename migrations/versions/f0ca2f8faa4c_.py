"""empty message

Revision ID: f0ca2f8faa4c
Revises: 5845f5ad19ac
Create Date: 2018-10-15 16:49:43.254518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0ca2f8faa4c'
down_revision = '5845f5ad19ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('good',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=240), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('is_calculated', sa.Boolean(), nullable=True),
    sa.Column('article', sa.String(length=60), nullable=True),
    sa.Column('img_src', sa.String(length=240), nullable=True),
    sa.Column('default', sa.Text(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('good')
    # ### end Alembic commands ###
