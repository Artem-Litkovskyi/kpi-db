import random
import glob
import os

import pandas as pd

from alpha_hash import alpha_hash
from btree import BTree


PATH_SURNAMES = 'surnames'


class TelNumberDB:
    def __init__(self):
        random_seed = 0
        random.seed(random_seed)

        # Load surnames
        all_files = glob.glob(os.path.join(PATH_SURNAMES, "*.txt"))
        self.df = pd.concat((pd.read_csv(f, header=None, names=['Surname']) for f in all_files), ignore_index=True)

        # Add random telephone numbers
        self.df['Tel'] = [random_tel() for i in self.df.index]

        # Shuffle
        self.df = self.df.sample(frac=1, random_state=random_seed).reset_index(drop=True)

        # Create surname index
        self.surname_index = BTree(alpha_hash)
        for row_id, row in self.df.iterrows():
            self.surname_index.insert(row['Surname'], row_id)

    def insert(self, surname: str, tel: str):
        self.df = self.df._append({'Surname': surname, 'Tel': tel}, ignore_index=True)
        self.surname_index.insert(surname, self.df.index.max())

    def search_by_surname(self, surname: str):
        match_ids = self.surname_index.search(surname)
        for row in map(lambda row_id: self.df.iloc[row_id], match_ids):
            if row['Surname'] != surname:
                continue
            yield row

    def search_by_surname_less(self, surname: str):
        # Lower hash
        match_ids = self.surname_index.search_less(surname)
        for row in map(lambda row_id: self.df.iloc[row_id], match_ids):
            yield row

        # Same hash
        match_ids = self.surname_index.search(surname)
        for row in map(lambda row_id: self.df.iloc[row_id], match_ids):
            if row['Surname'].lower() >= surname.lower():
                continue
            yield row
    
    def search_by_surname_greater(self, surname: str):
        # Same hash
        match_ids = self.surname_index.search(surname)
        for row in map(lambda row_id: self.df.iloc[row_id], match_ids):
            if row['Surname'].lower() <= surname.lower():
                continue
            yield row

        # Higher hash
        match_ids = self.surname_index.search_greater(surname)
        for row in map(lambda row_id: self.df.iloc[row_id], match_ids):
            yield row

def random_tel():
    first = str(random.randint(1, 999))
    second = str(random.randint(1, 99)).zfill(2)
    third = str(random.randint(1, 999)).zfill(3)
    fourth = str(random.randint(1, 99)).zfill(2)
    fifth = str(random.randint(1, 99)).zfill(2)
    return '+{}-{}-{}-{}-{}'.format(first, second, third, fourth, fifth)
