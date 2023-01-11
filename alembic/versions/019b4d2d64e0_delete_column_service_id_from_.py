"""Delete column service_id from servicekey table

Revision ID: 019b4d2d64e0
Revises: b480eb1b798c
Create Date: 2023-01-10 18:24:18.221586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '019b4d2d64e0'
down_revision = 'b480eb1b798c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint('key_service_fk', table_name='servicekey')
    op.drop_column('servicekey', 'service_id')


def downgrade() -> None:
    op.add_column(
        'service_key',
        sa.Column('service_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'key_service_fk', 
        source_table='servicekey',
        referent_table='service',
        local_cols=['service_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
