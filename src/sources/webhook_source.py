
import requests
import pandas as pd


WEBHOOK_EVENTS_URL = "http://127.0.0.1:8000/webhook/events"

WEBHOOK_COLUMNS = [
    "customer_id",
    "full_name",
    "email",
    "city",
    "created_at",
    "source",
    "ingested_at"
]


def extract_webhook_data():
    """
    Retrieve customer events received by the webhook server.
    """

    print("\n========== WEBHOOK DATA EXTRACTION ==========")

    try:
        response = requests.get(
            WEBHOOK_EVENTS_URL,
            timeout=15
        )

        response.raise_for_status()

        json_data = response.json()

        events = json_data["events"]

        # Preserve the expected schema even when no events exist
        df = pd.DataFrame(
            events,
            columns=WEBHOOK_COLUMNS
        )

        print(f"Webhook URL: {WEBHOOK_EVENTS_URL}")
        print(f"HTTP Status Code: {response.status_code}")
        print(f"Total events extracted: {len(df)}")

        if df.empty:
            print("No webhook events are currently available.")
        else:
            print("\nExtracted webhook events:")
            print(df)

        return df

    except requests.exceptions.RequestException as error:
        print(f"Webhook extraction failed: {error}")
        raise


if __name__ == "__main__":
    extract_webhook_data()
