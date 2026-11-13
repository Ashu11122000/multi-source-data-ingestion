
import sqlite3
import pandas as pd
from pathlib import Path


def extract_sqlite_data():
    """
    Extract customer records from a SQLite database.
    """

    # Locate project root
    project_root = Path(__file__).resolve().parents[2]

    # Define database location
    db_path = project_root / "data" / "sqlite" / "source.db"

    # Establish database connection
    connection = sqlite3.connect(db_path)

    try:
        # Extract records using Pandas
        query = "SELECT * FROM customers"

        df = pd.read_sql_query(query, connection)

        print("\n========== SQLITE DATA EXTRACTION ==========")
        print(f"Source: {db_path}")
        print(f"Total records extracted: {len(df)}")

        print("\nExtracted customer data:")
        print(df)

        print("\nData types:")
        print(df.dtypes)

        return df

    finally:
        # Always close the database connection
        connection.close()


if __name__ == "__main__":
    extract_sqlite_data()
