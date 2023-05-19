"""final release

Revision ID: 59c0d463f723
Revises:
Create Date: 2023-01-13 15:59:54.011151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59c0d463f723'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'service',
        sa.Column(
            'id', sa.Integer(), nullable=False, index=True, primary_key=True
        ),
        sa.Column('name', sa.String(), nullable=False)
    )
    op.create_table(
        'serviceversion',
        sa.Column(
            'id', sa.Integer(), nullable=False, index=True, primary_key=True
        ),
        sa.Column('service_id', sa.Integer(), nullable=False),
        sa.Column('version', sa.String(), nullable=False),
        sa.Column('is_used', sa.Boolean(), nullable=False)
    )
    op.create_foreign_key(
        'service_fk',
        source_table='serviceversion',
        referent_table='service',
        local_cols=['service_id'],
        remote_cols=['id']
    )
    op.create_table(
        'servicekey',
        sa.Column(
            'id', sa.Integer(), nullable=False, index=True, primary_key=True
        ),
        sa.Column('version_id', sa.Integer(), nullable=False),
        sa.Column('service_key', sa.String(), nullable=False),
        sa.Column('service_value', sa.String(), nullable=False)
    )
    op.create_foreign_key(
        'service_version_fk',
        source_table='servicekey',
        referent_table='serviceversion',
        local_cols=['version_id'],
        remote_cols=['id']
    )


def downgrade() -> None:
    op.drop_constraint('service_version_fk', table_name='servicekey')
    op.drop_constraint('service_fk', table_name='serviceversion')
    op.drop_table('servicekey')
    op.drop_table('serviceversion')
    op.drop_table('service')
