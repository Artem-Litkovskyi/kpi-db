from sqlalchemy import Engine, inspect, select
from sqlalchemy.orm import Session

from domain import models
from service.csv_service import CsvService


class WeatherService:
    def __init__(self, engine: Engine, csv_service: CsvService):
        self.engine = engine
        self.csv_service = csv_service

    # === CREATE ============================================================================
    def load_from_csv(self):
        with Session(self.engine) as session, session.begin():
            session.query(models.Weather).delete()

            mapper = inspect(models.Weather)
            session.bulk_insert_mappings(mapper, self.csv_service.get_all(mapper))

    # === READ ==============================================================================
    def view_all(self, page, per_page):
        stmt = select(models.Weather).limit(per_page).offset(page * per_page)
        with Session(self.engine) as session, session.begin():
            for obj in session.execute(stmt):
                yield obj

    # === DELETE ============================================================================
    def delete_all(self):
        with Session(self.engine) as session, session.begin():
            num_rows_deleted = session.query(models.Weather).delete()

        return num_rows_deleted

    def delete_by_id(self, obj_id: int):
        with Session(self.engine) as session, session.begin():
            num_rows_deleted = session.query(models.Weather).filter_by(id=obj_id).delete()

        return num_rows_deleted
