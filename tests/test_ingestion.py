
import pandas as pd
import pytest

import main as ingestion_main


@pytest.fixture
def source_data():

    csv_df = pd.DataFrame([{
        "customer_id": "C001",
        "full_name": "Rahul Sharma",
        "email": "rahul@example.com",
        "city": "Delhi",
        "created_at": "2026-01-10",
    }])

    sqlite_df = pd.DataFrame([{
        "customer_id": 101,
        "customer_name": "Rohit Sharma",
        "email": "rohit@example.com",
        "country": "India",
        "registration_date": "2026-02-01",
    }])

    api_df = pd.DataFrame([{
        "id": 1,
        "name": "Leanne Graham",
        "email": "leanne@example.com",
        "address.city": "Gwenborough",
    }])

    webhook_df = pd.DataFrame([{
        "customer_id": "W001",
        "full_name": "Aarav Sharma",
        "email": "aarav@example.com",
        "city": "Panchkula",
        "created_at": "2026-03-01",
        "source": "webhook",
        "ingested_at": "2026-11-13T05:06:49+00:00",
    }])

    return csv_df, sqlite_df, api_df, webhook_df


def install_mock_extractors(monkeypatch, source_data):

    csv_df, sqlite_df, api_df, webhook_df = source_data

    monkeypatch.setattr(
        ingestion_main,
        "extract_csv_data",
        lambda: csv_df.copy()
    )

    monkeypatch.setattr(
        ingestion_main,
        "extract_sqlite_data",
        lambda: sqlite_df.copy()
    )

    monkeypatch.setattr(
        ingestion_main,
        "extract_api_data",
        lambda: api_df.copy()
    )

    monkeypatch.setattr(
        ingestion_main,
        "extract_webhook_data",
        lambda: webhook_df.copy()
    )


def test_pipeline_combines_all_four_sources(
    monkeypatch,
    source_data
):

    install_mock_extractors(monkeypatch, source_data)

    loaded = {}

    def fake_loader(df):

        loaded["data"] = df.copy()

        return len(df)

    monkeypatch.setattr(
        ingestion_main,
        "load_to_staging",
        fake_loader
    )

    result = ingestion_main.run_ingestion_pipeline()

    assert len(result) == 4
    assert len(loaded["data"]) == 4

    assert set(result["source"]) == {
        "csv",
        "sqlite",
        "api",
        "webhook"
    }

    assert result["record_id"].is_unique

    assert result["email"].notna().all()
    assert result["full_name"].notna().all()
    assert result["location"].notna().all()


def test_pipeline_creates_source_prefixed_record_ids(
    monkeypatch,
    source_data
):

    install_mock_extractors(monkeypatch, source_data)

    monkeypatch.setattr(
        ingestion_main,
        "load_to_staging",
        lambda df: len(df)
    )

    result = ingestion_main.run_ingestion_pipeline()

    assert set(result["record_id"]) == {
        "csv_C001",
        "sqlite_101",
        "api_1",
        "webhook_W001"
    }


def test_pipeline_calls_staging_loader(
    monkeypatch,
    source_data
):

    install_mock_extractors(monkeypatch, source_data)

    loader_calls = []

    def fake_loader(df):

        loader_calls.append(df.copy())

        return len(df)

    monkeypatch.setattr(
        ingestion_main,
        "load_to_staging",
        fake_loader
    )

    result = ingestion_main.run_ingestion_pipeline()

    assert len(loader_calls) == 1

    pd.testing.assert_frame_equal(
        loader_calls[0],
        result
    )


def test_pipeline_rejects_duplicate_record_ids(
    monkeypatch,
    source_data
):

    csv_df, sqlite_df, api_df, webhook_df = source_data

    duplicate_csv = pd.concat(
        [csv_df, csv_df],
        ignore_index=True
    )

    modified_sources = (
        duplicate_csv,
        sqlite_df,
        api_df,
        webhook_df
    )

    install_mock_extractors(
        monkeypatch,
        modified_sources
    )

    loader_called = {"value": False}

    def fake_loader(df):

        loader_called["value"] = True

        return len(df)

    monkeypatch.setattr(
        ingestion_main,
        "load_to_staging",
        fake_loader
    )

    with pytest.raises(ValueError, match="Duplicate"):

        ingestion_main.run_ingestion_pipeline()

    assert loader_called["value"] is False
