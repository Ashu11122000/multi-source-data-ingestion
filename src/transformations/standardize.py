
import pandas as pd
from datetime import datetime, timezone


def standardize_data(df, source):
    """
    Standardize records from different source systems
    into a common customer schema.
    """

    standardized = pd.DataFrame()

    if source == "csv":
        standardized["source_id"] = df["customer_id"].astype(str)
        standardized["full_name"] = df["full_name"]
        standardized["email"] = df["email"]
        standardized["location"] = df["city"]
        standardized["created_at"] = df["created_at"]

    elif source == "sqlite":
        standardized["source_id"] = df["customer_id"].astype(str)
        standardized["full_name"] = df["customer_name"]
        standardized["email"] = df["email"]
        standardized["location"] = df["country"]
        standardized["created_at"] = df["registration_date"]

    elif source == "api":
        standardized["source_id"] = df["id"].astype(str)
        standardized["full_name"] = df["name"]
        standardized["email"] = df["email"]
        standardized["location"] = df["address.city"]
        standardized["created_at"] = pd.NA

    elif source == "webhook":
        standardized["source_id"] = df["customer_id"].astype(str)
        standardized["full_name"] = df["full_name"]
        standardized["email"] = df["email"]
        standardized["location"] = df["city"]
        standardized["created_at"] = df["created_at"]

    else:
        raise ValueError(f"Unsupported source: {source}")

    standardized["source"] = source

    standardized["created_at"] = pd.to_datetime(
        standardized["created_at"],
        errors="coerce",
        utc=True
    )

    standardized["ingested_at"] = datetime.now(
        timezone.utc
    )

    return standardized
