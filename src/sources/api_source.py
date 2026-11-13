
import requests
import pandas as pd


API_URL = "https://jsonplaceholder.typicode.com/users"


def extract_api_data():
    """
    Extract user records from a public REST API.
    """

    print("\n========== REST API DATA EXTRACTION ==========")

    try:
        # Send GET request to the API
        response = requests.get(API_URL, timeout=15)

        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()

        # Convert JSON response into Python objects
        json_data = response.json()

        # Convert JSON records into Pandas DataFrame
        df = pd.json_normalize(json_data)

        print(f"API URL: {API_URL}")
        print(f"HTTP Status Code: {response.status_code}")
        print(f"Total records extracted: {len(df)}")

        print("\nExtracted API data:")
        print(df[["id", "name", "username", "email"]])

        print("\nData types:")
        print(df.dtypes)

        return df

    except requests.exceptions.RequestException as error:
        print(f"API request failed: {error}")
        raise


if __name__ == "__main__":
    extract_api_data()
