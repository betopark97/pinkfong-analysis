# System
import os
from dotenv import load_dotenv

# Database
from sqlalchemy import create_engine

# Utils
from utils import db_utils


def main():
    # Load env variables from .env
    load_dotenv()
    
    # Import interim data to postgres
    data_path = "../data/interim"
    db_params = {
        "host": "127.0.0.1",
        "database": "pinkfong_db",
        "user": "postgres",
        "password": os.environ.get("PASSWORD"),
        "port": "5432",
    }
    engine = create_engine(
        f'postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}/{db_params["database"]}'
    )
    db_utils.import_data_directory_to_postgres(data_path, engine)
    
if __name__ == "__main__":
    main()