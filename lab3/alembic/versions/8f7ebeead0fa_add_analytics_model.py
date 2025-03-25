"""Add Analytics model

Revision ID: 8f7ebeead0fa
Revises: 750b287f4cbd
Create Date: 2025-03-25 16:27:37.500512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from domain import models


# revision identifiers, used by Alembic.
revision: str = '8f7ebeead0fa'
down_revision: Union[str, None] = '750b287f4cbd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    analytics = op.create_table(
        'analytics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('should_go_outside', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['weather.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    conn = op.get_bind()
    res = conn.execute(sa.text(
        'SELECT weather.id, wind_kph, air_quality_us_epa_index '
        'FROM weather INNER JOIN air_quality ON weather.id = air_quality.id'
    ))

    op.bulk_insert(
        analytics,
        [{'id': r[0], 'should_go_outside': models.Analytics.get_should_go_outside(r[1], r[2])} for r in res]
    )


def downgrade() -> None:
    op.drop_table('analytics')
