
import pandas as pd
import pytest

from transformations.standardize import standardize_data


EXPECTED_COLUMNS = [
    "source_id",
    "full_name",
    "email",
    "location",
    "created_at",
    "source",
    "ingested_at",
]


@pytest.fixture
def csv_data():
    return pd.DataFrame([{
        "customer_id": "C001",
        "full_name": "Rahul Sharma",
        "email": "rahul@example.com",
        "city": "Delhi",
        "created_at": "2026-01-10",
    }])


@pytest.fixture
def sqlite_data():
    return pd.DataFrame([{
        "customer_id": 101,
        "customer_name": "Rohit Sharma",
        "email": "rohit@example.com",
        "country": "India",
        "registration_date": "2026-02-01",
    }])


@pytest.fixture
def api_data():
    return pd.DataFrame([{
        "id": 1,
        "name": "Leanne Graham",
        "email": "leanne@example.com",
        "address.city": "Gwenborough",
    }])


@pytest.fixture
def webhook_data():
    return pd.DataFrame([{
        "customer_id": "W001",
        "full_name": "Aarav Sharma",
        "email": "aarav@example.com",
        "city": "Panchkula",
        "created_at": "2026-03-01",
        "source": "webhook",
        "ingested_at": "2026-11-13T05:06:49+00:00",
    }])


def assert_common_schema(result, expected_source, expected_id):

    assert list(result.columns) == EXPECTED_COLUMNS
    assert len(result) == 1

    assert result.loc[0, "source"] == expected_source
    assert result.loc[0, "source_id"] == expected_id

    assert pd.notna(result.loc[0, "ingested_at"])

    assert str(result["created_at"].dtype).startswith(
        "datetime64"
    )


def test_standardize_csv_source(csv_data):

    result = standardize_data(csv_data, "csv")

    assert_common_schema(result, "csv", "C001")

    assert result.loc[0, "full_name"] == "Rahul Sharma"
    assert result.loc[0, "location"] == "Delhi"
    assert result.loc[0, "email"] == "rahul@example.com"

    assert result.loc[0, "created_at"] == pd.Timestamp(
        "2026-01-10",
        tz="UTC"
    )


def test_standardize_sqlite_source(sqlite_data):

    result = standardize_data(sqlite_data, "sqlite")

    assert_common_schema(result, "sqlite", "101")

    assert result.loc[0, "full_name"] == "Rohit Sharma"
    assert result.loc[0, "location"] == "India"

    assert result.loc[0, "created_at"] == pd.Timestamp(
        "2026-02-01",
        tz="UTC"
    )


def test_standardize_api_source(api_data):

    result = standardize_data(api_data, "api")

    assert_common_schema(result, "api", "1")

    assert result.loc[0, "full_name"] == "Leanne Graham"
    assert result.loc[0, "location"] == "Gwenborough"

    # API does not provide a customer registration date.
    assert pd.isna(result.loc[0, "created_at"])


def test_standardize_webhook_source(webhook_data):

    result = standardize_data(webhook_data, "webhook")

    assert_common_schema(result, "webhook", "W001")

    assert result.loc[0, "full_name"] == "Aarav Sharma"
    assert result.loc[0, "location"] == "Panchkula"

    assert result.loc[0, "created_at"] == pd.Timestamp(
        "2026-03-01",
        tz="UTC"
    )


def test_invalid_source_raises_value_error(csv_data):

    with pytest.raises(ValueError):

        standardize_data(csv_data, "unknown_source")


def test_invalid_date_is_converted_to_nat(csv_data):

    csv_data.loc[0, "created_at"] = "not-a-date"

    result = standardize_data(csv_data, "csv")

    assert pd.isna(result.loc[0, "created_at"])


def test_source_id_is_always_string(sqlite_data):

    result = standardize_data(sqlite_data, "sqlite")

    assert result.loc[0, "source_id"] == "101"
    assert isinstance(result.loc[0, "source_id"], str)
