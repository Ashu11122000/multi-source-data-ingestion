
import pandas as pd
from pathlib import Path


def extract_csv_data():
    """
    Extract customer records from a CSV file.
    """

    # Locate the project root directory
    project_root = Path(__file__).resolve().parents[2]

    # Define CSV file location
    csv_path = project_root / "data" / "csv" / "customers.csv"

    # Read CSV file using Pandas
    df = pd.read_csv(csv_path)

    print("\n========== CSV DATA EXTRACTION ==========")
    print(f"Source: {csv_path}")
    print(f"Total records extracted: {len(df)}")

    print("\nExtracted customer data:")
    print(df)

    print("\nData types:")
    print(df.dtypes)

    return df


if __name__ == "__main__":
    extract_csv_data()
