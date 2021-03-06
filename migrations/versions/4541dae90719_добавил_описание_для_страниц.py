"""добавил описание для страниц

Revision ID: 4541dae90719
Revises: 86e60f8d0804
Create Date: 2019-01-14 00:57:57.686653

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4541dae90719'
down_revision = '86e60f8d0804'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article_pages', sa.Column('page_description', sa.Text(), nullable=False))
    op.alter_column('article_pages', 'page_name',
               existing_type=mysql.TEXT(collation='utf8mb4_unicode_ci'),
               nullable=False)
    op.alter_column('article_pages', 'page_transcription',
               existing_type=mysql.TEXT(collation='utf8mb4_unicode_ci'),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article_pages', 'page_transcription',
               existing_type=mysql.TEXT(collation='utf8mb4_unicode_ci'),
               nullable=True)
    op.alter_column('article_pages', 'page_name',
               existing_type=mysql.TEXT(collation='utf8mb4_unicode_ci'),
               nullable=True)
    op.drop_column('article_pages', 'page_description')
    # ### end Alembic commands ###
