"""Add Weather model

Revision ID: 00930292790a
Revises: 
Create Date: 2025-03-23 19:28:39.924510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00930292790a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _get_compass16():
    return sa.Enum(
        'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW',
        name='compass16',
        create_type=False
    )


def upgrade() -> None:
    # compass16 = _get_compass16()
    # compass16.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'weather',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('country', sa.String(length=50), nullable=False),
        sa.Column('last_updated', sa.DateTime(), nullable=False),
        sa.Column('wind_degree', sa.Integer(), nullable=False),
        sa.Column('wind_kph', sa.Float(), nullable=False),
        sa.Column('wind_direction', sa.Enum(
            'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW',
            name='compass16',
            create_type=False
        ), nullable=False),
        sa.Column('sunrise', sa.DateTime(), nullable=False),
        sa.Column('air_quality_carbon_monoxide', sa.Float(), nullable=False),
        sa.Column('air_quality_ozone', sa.Float(), nullable=False),
        sa.Column('air_quality_nitrogen_dioxide', sa.Float(), nullable=False),
        sa.Column('air_quality_sulphur_dioxide', sa.Float(), nullable=False),
        sa.Column('air_quality_pm2_5', sa.Float(), nullable=False),
        sa.Column('air_quality_pm10', sa.Float(), nullable=False),
        sa.Column('air_quality_us_epa_index', sa.Integer(), nullable=False),
        sa.Column('air_quality_gb_defra_index', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('weather')

    compass16 = _get_compass16()
    compass16.drop(op.get_bind())
