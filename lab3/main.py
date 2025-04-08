from sqlalchemy import create_engine, event

import config
from presentation.text_ui import TextUI
from service.csv_service import CsvService
from service.weather_service import WeatherService
from repository.csv_repository import CsvRepository
from repository.weather_repository import WeatherRepository


# Repository
engine = create_engine(config.ENGINE_URL)


# Stop MySQL from swapping id=0 with an automatic id
@event.listens_for(engine, "connect", insert=True)
def connect(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO'")


csv_repository = CsvRepository(config.CSV_PATH)
weather_repository = WeatherRepository(engine)


# Service
csv_service = CsvService(csv_repository)
weather_service = WeatherService(weather_repository, csv_service)


# Presentation
text_ui = TextUI(weather_service)


text_ui.main_menu()
