from sqlalchemy import Engine


class WeatherRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
