
import sqlite3
from pathlib import Path


# Locate project root
project_root = Path(__file__).resolve().parents[2]

# Define database path
db_path = project_root / "data" / "sqlite" / "source.db"


def create_database():

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            email TEXT NOT NULL,
            country TEXT,
            registration_date TEXT
        )
    """)

    # Insert mock records
    customers = [
        (101, "Rohit Sharma", "rohit@example.com", "India", "2026-02-01"),
        (102, "Sneha Patel", "sneha@example.com", "India", "2026-02-03"),
        (103, "Vikram Singh", "vikram@example.com", "India", "2026-02-05"),
        (104, "Pooja Mehta", "pooja@example.com", "India", "2026-02-08"),
        (105, "Aditya Verma", "aditya@example.com", "India", "2026-02-10")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO customers
        VALUES (?, ?, ?, ?, ?)
    """, customers)

    connection.commit()
    connection.close()

    print("SQLite database created successfully!")
    print(f"Database location: {db_path}")
    print("5 customer records inserted.")


if __name__ == "__main__":
    create_database()
