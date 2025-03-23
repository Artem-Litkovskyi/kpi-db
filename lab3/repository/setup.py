from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists


ENGINE_URL = 'postgresql://postgres:123@localhost/lab3'


def validate_database():
    engine = create_engine(ENGINE_URL)
    if not database_exists(engine.url):  # Checks for the first time
        create_database(engine.url)  # Create a new DB
        print('New Database Created', database_exists(engine.url))  # Verifies if database is there or not.
    else:
        print('Database Already Exists')
