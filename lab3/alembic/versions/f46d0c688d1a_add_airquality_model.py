"""Add AirQuality model

Revision ID: f46d0c688d1a
Revises: 00930292790a
Create Date: 2025-03-25 10:07:23.277080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f46d0c688d1a'
down_revision: Union[str, None] = '00930292790a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'air_quality',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('air_quality_carbon_monoxide', sa.Float(), nullable=False),
        sa.Column('air_quality_ozone', sa.Float(), nullable=False),
        sa.Column('air_quality_nitrogen_dioxide', sa.Float(), nullable=False),
        sa.Column('air_quality_sulphur_dioxide', sa.Float(), nullable=False),
        sa.Column('air_quality_pm2_5', sa.Float(), nullable=False),
        sa.Column('air_quality_pm10', sa.Float(), nullable=False),
        sa.Column('air_quality_us_epa_index', sa.Integer(), nullable=False),
        sa.Column('air_quality_gb_defra_index', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['weather.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('air_quality')
