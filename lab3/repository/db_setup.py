from sqlalchemy import Engine
from sqlalchemy_utils import create_database, database_exists


def validate_database_existence(engine: Engine):
    if not database_exists(engine.url):  # Checks for the first time
        create_database(engine.url)  # Create a new DB
        print('New Database Created', database_exists(engine.url))  # Verifies if database is there or not.
    else:
        print('Database Already Exists')
