"""Add fk constraint

Revision ID: 506dd116adff
Revises: c75a996fcfd6
Create Date: 2022-11-18 15:23:36.152676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '506dd116adff'
down_revision = 'c75a996fcfd6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key(
        'version_service_fk',
        source_table='serviceversion',
        referent_table='service',
        local_cols=['service_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'key_service_fk',
        source_table='servicekey',
        referent_table='service',
        local_cols=['service_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'key_version_fk',
        source_table='servicekey',
        referent_table='serviceversion',
        local_cols=['version_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('version_service_fk', table_name='serviceversion')
    op.drop_constraint('key_service_fk', table_name='servicekey')
    op.drop_constraint('key_version_fk', table_name='servicekey')
