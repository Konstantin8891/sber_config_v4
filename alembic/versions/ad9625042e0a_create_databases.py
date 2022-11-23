"""Create databases

Revision ID: ad9625042e0a
Revises: 
Create Date: 2022-11-17 16:47:10.130396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad9625042e0a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'service',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False)
    )
    op.create_table(
        'serviceversion',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('version', sa.String(), nullable=False),
        sa.Column('is_used', sa.Boolean(), nullable=False)
    )
    op.create_table(
        'servicekey',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('service_key', sa.String(), nullable=False),
        sa.Column('service_value', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('service')
    op.drop_table('serviceversion')
    op.drop_table('servicekey')

