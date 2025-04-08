import pandas as pd

from repository.csv_repository import CsvRepository


class CsvService:
    def __init__(self, csv_repository: CsvRepository):
        self.csv_repository = csv_repository

    def get_all(self) -> pd.DataFrame:
        return self.csv_repository.read_all()
