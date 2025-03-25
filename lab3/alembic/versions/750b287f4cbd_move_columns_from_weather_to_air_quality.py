"""Move columns from weather to air_quality

Revision ID: 750b287f4cbd
Revises: f46d0c688d1a
Create Date: 2025-03-25 11:38:12.403011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '750b287f4cbd'
down_revision: Union[str, None] = 'f46d0c688d1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    weather_name = 'weather'
    air_quality_name = 'air_quality'

    # Reflect tables
    conn = op.get_bind()
    meta = sa.MetaData()
    meta.reflect(bind=conn, only=(weather_name, air_quality_name))
    air_quality = sa.Table(air_quality_name, meta)

    # Move columns from weather to air_quality
    columns = [c.name for c in air_quality.columns]
    res = conn.execute(sa.text(f'SELECT {', '.join(columns)} FROM {weather_name}'))
    op.execute(f'TRUNCATE TABLE {air_quality_name}')
    op.bulk_insert(air_quality, [{columns[i]: r[i] for i in range(len(columns))} for r in res])

    for c in columns:
        if c == 'id':
            continue
        op.drop_column(weather_name, c)


def downgrade() -> None:
    weather_name = 'weather'
    air_quality_name = 'air_quality'

    # Reflect tables
    conn = op.get_bind()
    meta = sa.MetaData()
    meta.reflect(bind=conn, only=(weather_name, air_quality_name))
    air_quality = sa.Table(air_quality_name, meta)

    # Move columns from air_quality to weather
    columns = [c.name for c in air_quality.columns]
    res = conn.execute(sa.text(f'SELECT {', '.join(columns)} FROM {air_quality_name}'))

    for c in air_quality.columns:
        if c.name == 'id':
            continue
        c.server_default = '0'
        op.add_column(weather_name, c)

    for r in res:
        tmp = ', '.join('%s = %s' % (columns[i], r[i]) for i in range(len(columns)) if columns[i] != 'id')
        op.execute(f'UPDATE {weather_name} SET {tmp} WHERE id = {r[columns.index('id')]}')

    op.execute(f'TRUNCATE TABLE {air_quality_name}')