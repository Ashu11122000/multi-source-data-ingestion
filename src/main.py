
import pandas as pd

# Import extraction functions
from sources.csv_source import extract_csv_data
from sources.sqlite_source import extract_sqlite_data
from sources.api_source import extract_api_data
from sources.webhook_source import extract_webhook_data

# Import transformation function
from transformations.standardize import standardize_data

# Import staging loader
from loaders.staging_loader import load_to_staging


def run_ingestion_pipeline():
    """
    Unified multi-source data ingestion pipeline.

    Workflow:
    Extract -> Standardize -> Validate ->
    Consolidate -> Load into SQLite staging
    """

    print("\n" + "=" * 65)
    print("          UNIFIED MULTI-SOURCE DATA INGESTION")
    print("=" * 65)

    # ==========================================
    # 1. DATA EXTRACTION
    # ==========================================

    print("\n========== PHASE 1: DATA EXTRACTION ==========")

    csv_df = extract_csv_data()

    sqlite_df = extract_sqlite_data()

    api_df = extract_api_data()

    webhook_df = extract_webhook_data()

    # ==========================================
    # 2. DATA STANDARDIZATION
    # ==========================================

    print("\n========== PHASE 2: DATA STANDARDIZATION ==========")

    csv_standardized = standardize_data(csv_df, "csv")

    sqlite_standardized = standardize_data(
        sqlite_df, "sqlite"
    )

    api_standardized = standardize_data(api_df, "api")

    webhook_standardized = standardize_data(
        webhook_df, "webhook"
    )

    print("CSV standardization completed.")
    print("SQLite standardization completed.")
    print("REST API standardization completed.")
    print("Webhook standardization completed.")

    # ==========================================
    # 3. DATA CONSOLIDATION
    # ==========================================

    print("\n========== PHASE 3: DATA CONSOLIDATION ==========")

    unified_df = pd.concat(
        [
            csv_standardized,
            sqlite_standardized,
            api_standardized,
            webhook_standardized
        ],
        ignore_index=True
    )

    # Generate source-specific record identifiers
    unified_df.insert(
        0,
        "record_id",
        unified_df["source"] + "_" + unified_df["source_id"]
    )

    print(f"Total consolidated records: {len(unified_df)}")

    # ==========================================
    # 4. DATA QUALITY VALIDATION
    # ==========================================

    print("\n========== PHASE 4: DATA QUALITY VALIDATION ==========")

    duplicate_count = unified_df["record_id"].duplicated().sum()

    missing_email_count = unified_df["email"].isna().sum()

    missing_name_count = unified_df["full_name"].isna().sum()

    missing_location_count = unified_df["location"].isna().sum()

    print(f"Total records: {len(unified_df)}")
    print(f"Duplicate record IDs: {duplicate_count}")
    print(f"Missing emails: {missing_email_count}")
    print(f"Missing names: {missing_name_count}")
    print(f"Missing locations: {missing_location_count}")

    # Stop loading if duplicate record IDs exist
    if duplicate_count > 0:
        raise ValueError(
            "Duplicate record IDs detected. "
            "Staging load cancelled."
        )

    # ==========================================
    # 5. SOURCE-WISE SUMMARY
    # ==========================================

    print("\n========== PHASE 5: SOURCE-WISE SUMMARY ==========")

    source_summary = (
        unified_df.groupby("source")
        .size()
        .rename("record_count")
    )

    print(source_summary)

    # ==========================================
    # 6. DISPLAY UNIFIED DATASET
    # ==========================================

    print("\n========== UNIFIED STANDARDIZED DATASET ==========")

    print(unified_df.to_string(index=False))

    print("\nFinal column data types:")
    print(unified_df.dtypes)

    # ==========================================
    # 7. LOAD INTO SQLITE STAGING
    # ==========================================

    print("\n========== PHASE 6: STAGING DATA LOAD ==========")

    loaded_records = load_to_staging(unified_df)

    # ==========================================
    # 8. FINAL PIPELINE SUMMARY
    # ==========================================

    print("\n" + "=" * 65)
    print("             INGESTION PIPELINE SUMMARY")
    print("=" * 65)

    print(f"CSV records:       {len(csv_df)}")
    print(f"SQLite records:    {len(sqlite_df)}")
    print(f"API records:       {len(api_df)}")
    print(f"Webhook records:   {len(webhook_df)}")

    print("-" * 65)

    print(f"Total extracted:   {len(unified_df)}")
    print(f"Total loaded:      {loaded_records}")

    if loaded_records == len(unified_df):
        print("\nPIPELINE STATUS: SUCCESS")
    else:
        print("\nPIPELINE STATUS: WARNING - Record count mismatch")

    print("=" * 65)

    return unified_df


if __name__ == "__main__":
    unified_data = run_ingestion_pipeline()
