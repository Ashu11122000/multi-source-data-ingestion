
import sqlite3
import pandas as pd
from pathlib import Path


def load_to_staging(df):
    """
    Load unified customer records into SQLite staging.
    """

    # Locate project root
    project_root = Path(__file__).resolve().parents[2]

    # Define staging database path
    staging_db = (
        project_root / "data" / "staging" / "staging.db"
    )

    # Create staging directory if necessary
    staging_db.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print("\n========== STAGING DATA LOAD ==========")

    connection = sqlite3.connect(staging_db)

    try:
        # Convert datetime columns for SQLite storage
        staging_df = df.copy()

        for column in ["created_at", "ingested_at"]:
            staging_df[column] = (
                staging_df[column].astype("string")
            )

        # Load records into SQLite
        staging_df.to_sql(
            name="unified_customers",
            con=connection,
            if_exists="replace",
            index=False
        )

        # Verify inserted record count
        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM unified_customers"
        )

        record_count = cursor.fetchone()[0]

        print(f"Staging database: {staging_db}")
        print(f"Table: unified_customers")
        print(f"Records loaded: {record_count}")

        return record_count

    finally:
        connection.close()


if __name__ == "__main__":
    print("Import load_to_staging() from main.py to load data.")
