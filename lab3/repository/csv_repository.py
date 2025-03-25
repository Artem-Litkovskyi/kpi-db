import pandas as pd
from datetime import datetime

from domain import models


class CsvRepository:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def read_all(self) -> pd.DataFrame:
        df = pd.read_csv(self.csv_path)

        # Create a new column with index values
        df['id'] = df.index

        # Rename columns
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.replace('.', '_')
        df.columns = df.columns.str.replace('-', '_')

        # Convert strings to datetime
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        df['sunrise'] = df.apply(self.sunrise_to_datetime, axis=1)

        # Convert strings to enums
        df['wind_direction'] = df['wind_direction'].apply(lambda x: models.Compass16(x.lower()))

        return df

    @staticmethod
    def sunrise_to_datetime(row):
        dt = datetime.strptime(row['sunrise'], '%I:%M %p')

        dt = dt.replace(
            year=row['last_updated'].year,
            month=row['last_updated'].month,
            day=row['last_updated'].day,
        )

        return dt
