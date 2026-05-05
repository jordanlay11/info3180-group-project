"""Merging heads for db upgrade

Revision ID: 0e2a9cb4e333
Revises: c5f28cca8b29, 3c10a8dd909d
Create Date: 2026-05-05 17:03:23.054454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e2a9cb4e333'
down_revision = ('c5f28cca8b29', '3c10a8dd909d')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
