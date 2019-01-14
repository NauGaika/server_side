"""добавил описание для страниц

Revision ID: 55ad2e41ada4
Revises: 2ce7bacfece6
Create Date: 2019-01-14 01:54:11.510193

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '55ad2e41ada4'
down_revision = '2ce7bacfece6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article_img_containers', 'alt')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_img_containers', sa.Column('alt', mysql.TEXT(collation='utf8mb4_unicode_ci'), nullable=True))
    # ### end Alembic commands ###
