"""Add foreignkey constraint

Revision ID: c75a996fcfd6
Revises: ad9625042e0a
Create Date: 2022-11-17 17:15:53.613587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c75a996fcfd6'
down_revision = 'ad9625042e0a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'serviceversion',
        sa.Column('service_id', sa.Integer(), nullable=False)
    )
    op.add_column(
        'servicekey',
        sa.Column('service_id', sa.Integer(), nullable=False)
    )
    op.add_column(
        'servicekey',
        sa.Column('version_id', sa.Integer(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column('serviceversion', 'service_id')
    op.drop_column('servicekey', 'service_id')
    op.drop_column('servicekey', 'version_id')
