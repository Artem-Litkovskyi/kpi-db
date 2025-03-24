from repository.csv_repository import CsvRepository


class CsvService:
    def __init__(self, csv_repository: CsvRepository):
        self.csv_repository = csv_repository

    def get_all(self, model_mapper):
        df = self.csv_repository.read_all(model_mapper)

        for index, row in df.iterrows():
            yield dict(row)
