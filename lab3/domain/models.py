import enum
from datetime import datetime
from sqlalchemy import String, inspect, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Compass16(enum.StrEnum):
    N = enum.auto()
    NNE = enum.auto()
    NE = enum.auto()
    ENE = enum.auto()
    E = enum.auto()
    ESE = enum.auto()
    SE = enum.auto()
    SSE = enum.auto()
    S = enum.auto()
    SSW = enum.auto()
    SW = enum.auto()
    WSW = enum.auto()
    W = enum.auto()
    WNW = enum.auto()
    NW = enum.auto()
    NNW = enum.auto()


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        mapper = inspect(self.__class__)

        string = '%s(%s)' % (
            self.__class__.__name__,
            ', '.join('%s=%s' % (c.key, self.__dict__[c.key]) for c in mapper.column_attrs),
        )

        return string


class Weather(Base):
    __tablename__ = 'weather'

    id: Mapped[int] = mapped_column(primary_key=True)

    country: Mapped[str] = mapped_column(String(50))
    last_updated: Mapped[datetime]

    wind_degree: Mapped[int]
    wind_kph: Mapped[float]
    wind_direction: Mapped[Compass16]

    sunrise: Mapped[datetime]

    air_quality: Mapped['AirQuality'] = relationship(
        backref='weather',
        cascade='all, delete',
        passive_deletes=True
    )

    analytics: Mapped['Analytics'] = relationship(
        backref='weather',
        cascade='all, delete',
        passive_deletes=True
    )


class AirQuality(Base):
    __tablename__ = 'air_quality'

    id: Mapped[int] = mapped_column(ForeignKey(Weather.id, ondelete='CASCADE'), primary_key=True)

    air_quality_carbon_monoxide: Mapped[float]
    air_quality_ozone: Mapped[float]
    air_quality_nitrogen_dioxide: Mapped[float]
    air_quality_sulphur_dioxide: Mapped[float]
    air_quality_pm2_5: Mapped[float]
    air_quality_pm10: Mapped[float]
    air_quality_us_epa_index: Mapped[int]
    air_quality_gb_defra_index: Mapped[int]


class Analytics(Base):
    __tablename__ = 'analytics'

    id: Mapped[int] = mapped_column(ForeignKey(Weather.id, ondelete='CASCADE'), primary_key=True)

    should_go_outside: Mapped[bool] = mapped_column(default=True)

    @staticmethod
    def get_analytics_dict(**kwargs):
        return {
            'id': kwargs['id'],
            'should_go_outside': kwargs['wind_kph'] < 80 and kwargs['air_quality_us_epa_index'] <= 3
        }
