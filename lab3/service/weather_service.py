from sqlalchemy import select, inspect, func
from sqlalchemy.orm import Session

from domain import models
from service.csv_service import CsvService
from repository.weather_repository import WeatherRepository


class WeatherService:
    def __init__(self, weather_repository: WeatherRepository, csv_service: CsvService):
        self.weather_repository = weather_repository
        self.csv_service = csv_service

    # === CREATE ============================================================================
    def load_from_csv(self):
        with Session(self.weather_repository.engine) as session, session.begin():
            session.query(models.Weather).delete()

            df = self.csv_service.get_all()

            for model in [models.Weather, models.AirQuality]:
                mapper = inspect(model)
                session.bulk_insert_mappings(
                    mapper,
                    ({c.key: row[c.key] for c in mapper.column_attrs} for _, row in df.iterrows())
                )

            mapper = inspect(models.Analytics)
            session.bulk_insert_mappings(
                mapper,
                (models.Analytics.get_analytics_dict(**row) for _, row in df.iterrows())
            )

    # === READ ==============================================================================
    def view_all(self, page: int, per_page: int):
        stmt = select(models.Weather).limit(per_page).offset(page * per_page)
        with Session(self.weather_repository.engine) as session, session.begin():
            for obj in session.execute(stmt):
                yield obj

    def search(self, country: str, year: int, month: int, day: int):
        stmt = (
            select(models.Weather)
            .filter(models.Weather.country.ilike(country))
            .filter(func.date(models.Weather.last_updated) == '%04i-%02i-%02i' % (year, month, day))
        )

        with Session(self.weather_repository.engine) as session, session.begin():
            for obj in session.execute(stmt):
                yield obj

    # === DELETE ============================================================================
    def delete_all(self):
        with Session(self.weather_repository.engine) as session, session.begin():
            num_rows_deleted = session.query(models.Weather).delete()

        return num_rows_deleted

    def delete_by_id(self, obj_id: int):
        with Session(self.weather_repository.engine) as session, session.begin():
            num_rows_deleted = session.query(models.Weather).filter_by(id=obj_id).delete()

        return num_rows_deleted
