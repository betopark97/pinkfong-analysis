# System
from pathlib import Path

# DataFrame
import pandas as pd

# Database
from sqlalchemy.engine import Engine


def import_data_directory_to_postgres(data_path: str, engine: Engine, extension: str = ".csv"):
    """
    Import CSV files from a given directory into a PostgreSQL database.

    Parameters
    ----------
    data_path : str
        Directory path containing the CSV files to import.
    engine : sqlalchemy.engine.Engine
        A SQLAlchemy engine object connected to a PostgreSQL database.
    extension : str, optional
        File extension to filter (default is '.csv').

    Returns
    -------
    None
    """
    try:
        # Define the file paths for your CSV files
        csv_files = {}
        data_files = Path(data_path).glob(f"*{extension}")  # Filter files by extension
        
        for file_path in data_files:
            table_name = file_path.stem  # Extract the file name without the extension
            csv_files[table_name] = file_path  # Store the full file path in the dictionary

        # Loop through the CSV files and import them into PostgreSQL
        for table_name, file_path in csv_files.items():
            try:
                df = pd.read_csv(file_path)  # Read the CSV file
                df.to_sql(table_name, engine, if_exists="replace", index=False)  # Load into PostgreSQL
                print(f"Table '{table_name}' imported successfully.")
            except Exception as e:
                print(f"Error importing table '{table_name}': {e}")

    except Exception as e:
        print(f"Error processing directory '{data_path}': {e}")