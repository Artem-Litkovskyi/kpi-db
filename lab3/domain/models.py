import enum
from datetime import datetime
from sqlalchemy import String, Enum, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
    pass


class Weather(Base):
    __tablename__ = 'weather'

    id: Mapped[int] = mapped_column(primary_key=True)

    country: Mapped[str] = mapped_column(String(50))
    last_updated: Mapped[datetime]

    wind_degree: Mapped[int]
    wind_kph: Mapped[float]
    wind_direction: Mapped[Compass16]

    sunrise: Mapped[datetime]

    air_quality_carbon_monoxide: Mapped[float]
    air_quality_ozone: Mapped[float]
    air_quality_nitrogen_dioxide: Mapped[float]
    air_quality_sulphur_dioxide: Mapped[float]
    air_quality_pm2_5: Mapped[float]
    air_quality_pm10: Mapped[float]
    air_quality_us_epa_index: Mapped[int]
    air_quality_gb_defra_index: Mapped[int]

    def __repr__(self) -> str:
        return (
            f'Weather(id={self.id}, country={self.country}, last_updated={self.last_updated}, \
            wind_degree={self.wind_degree}, wind_kph={self.wind_kph}, wind_direction={self.wind_direction}, \
            sunrise={self.sunrise}, \
            air_quality_us_epa_index={self.air_quality_us_epa_index}, \
            air_quality_gb_defra_index={self.air_quality_gb_defra_index})'
        )
