from sqlalchemy import create_engine

import config
from presentation.text_ui import TextUI
from service.csv_service import CsvService
from service.weather_service import WeatherService
from repository.csv_repository import CsvRepository


# Repository
engine = create_engine(config.ENGINE_URL)
csv_repository = CsvRepository(config.CSV_PATH)

# Service
csv_service = CsvService(csv_repository)
weather_service = WeatherService(engine, csv_service)

# Presentation
text_ui = TextUI(weather_service)


text_ui.main_menu()
