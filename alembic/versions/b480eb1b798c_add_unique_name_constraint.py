"""Add unique name constraint

Revision ID: b480eb1b798c
Revises: 506dd116adff
Create Date: 2022-11-18 16:31:08.702850

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'b480eb1b798c'
down_revision = '506dd116adff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint('uq_service_name', 'service', ['name'])


def downgrade() -> None:
    op.drop_constraint('uq_service_name', 'service')
