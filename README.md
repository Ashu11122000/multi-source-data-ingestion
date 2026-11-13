# Unified Multi-Source Data Ingestion Pipeline

## 1. Project Overview

This project demonstrates how data from multiple independent systems can be collected, standardized, validated, and stored in one unified staging repository.

Organizations rarely keep all their data in one place. Customer information may be maintained in CSV files, operational applications may use relational databases, external services may expose REST APIs, and business applications may send events through webhooks or message queues.

The objective of this project is to build a small local data-ingestion pipeline that demonstrates these different integration patterns using Python.

The pipeline integrates four mock data sources:

1. **CSV file:** customer records stored in a local comma-separated values file.
2. **SQLite database:** customer records stored in a local relational database.
3. **Public REST API:** user records retrieved from JSONPlaceholder.
4. **Webhook simulator:** customer events pushed to a local FastAPI endpoint.

The extracted records are mapped to a common customer schema, combined into one pandas DataFrame, checked for basic data-quality issues, and loaded into a SQLite staging database.

### Current execution result

The latest successful pipeline run produced:

| Source    | Records extracted |
| --------- | ----------------: |
| CSV       |                 8 |
| SQLite    |                 5 |
| REST API  |                10 |
| Webhook   |                 1 |
| **Total** |            **24** |

All 24 records were loaded into the staging table during that run.

---

## 2. Project Objectives

The main objectives are to:

- Set up a reproducible local Python development environment.
- Connect to four different source-system patterns.
- Extract structured data from files, databases, APIs, and pushed events.
- Standardize different field names and data types into a common schema.
- Consolidate records from all sources into one dataset.
- perform basic data-quality checks.
- Load the consolidated dataset into a centralized staging repository.
- Test transformation logic and the end-to-end ingestion pipeline.

---

## 3. Concepts Explained

### 3.1 Data ingestion

Data ingestion is the process of collecting data from one or more source systems and bringing it into a target environment for further processing, analytics, or storage.

An ingestion pipeline commonly includes extraction, transformation or standardization, validation, and loading.

### 3.2 Source systems

A source system is the original location or application from which data is collected.

This project uses four source types:

| Source   | What it represents                          | Integration approach                                      |
| -------- | ------------------------------------------- | --------------------------------------------------------- |
| CSV      | File-based data exchange                    | Read a local file                                         |
| SQLite   | Relational database                         | Execute a SQL query                                       |
| REST API | External application/service                | Send an HTTP GET request                                  |
| Webhook  | Event notification from another application | Receive an HTTP POST event, then retrieve received events |

### 3.3 Pull-based ingestion

In pull-based ingestion, the pipeline initiates the request to retrieve data.

Examples in this project:

- Reading the CSV file.
- Querying the SQLite database.
- Sending a GET request to the public REST API.
- Sending a GET request to retrieve events already received by the webhook simulator.

The ingestion process controls when it retrieves the data.

### 3.4 Push-based ingestion

In push-based ingestion, an external system sends data to an endpoint when an event occurs.

The local webhook simulator demonstrates this approach. A client sends a POST request to the FastAPI endpoint, and the application receives and stores the event in memory.

The pipeline later retrieves the received events through the webhook GET endpoint. Therefore, event delivery is push-based, while the pipeline's collection of the stored event list is pull-based.

### 3.5 Data standardization

Different source systems can represent the same business information using different field names and formats.

For example:

| Source   | Original customer-name field | Standardized field |
| -------- | ---------------------------- | ------------------ |
| CSV      | `full_name`                  | `full_name`        |
| SQLite   | `customer_name`              | `full_name`        |
| REST API | `name`                       | `full_name`        |
| Webhook  | `full_name`                  | `full_name`        |

Standardization maps these source-specific structures to a common schema.

### 3.6 Unified staging repository

A staging repository is a centralized location where extracted and standardized data is stored before downstream transformations, analytics, or reporting.

This project uses a SQLite database for the staging repository. The consolidated data is stored in the `unified_customers` table.

The current loader uses a full-refresh approach: it replaces the staging table on each run rather than incrementally appending records.

---

## 4. Technology Stack

| Technology     | Purpose                                                                                              |
| -------------- | ---------------------------------------------------------------------------------------------------- |
| Python         | Main programming language                                                                            |
| pandas         | Data extraction, transformation, standardization, and consolidation                                  |
| requests       | HTTP communication with REST endpoints                                                               |
| SQLite         | Local source database and staging repository                                                         |
| FastAPI        | Local webhook receiver                                                                               |
| Uvicorn        | Local ASGI server for FastAPI                                                                        |
| SQLAlchemy     | Installed as part of the project environment; not currently required by the ingestion implementation |
| pytest         | Automated testing                                                                                    |
| VS Code        | Development environment                                                                              |
| Git and GitHub | Version control and project hosting                                                                  |

---

## 5. Development Environment Setup

### Step 1: Create the project directory

Create a project directory named:

`multi-source-data-ingestion`

Open this directory in Visual Studio Code.

### Step 2: Create a Python virtual environment

Create a virtual environment named `.venv` in the project root.

Activate the environment before installing dependencies or running the application.

### Step 3: Install project dependencies

Install the packages recorded in `requirements.txt`.

The primary runtime dependencies are pandas, requests, FastAPI, Uvicorn, and email-validator. pytest is used for automated tests.

### Step 4: Prepare the source and staging directories

Create separate directories for:

- CSV source files.
- SQLite source database.
- Staging database.
- Source extraction modules.
- Transformation modules.
- Loader modules.
- Webhook application.
- Automated tests.
- Project documentation.

### Step 5: Generate the SQLite source database

Run the SQLite database setup utility. It creates the source database and its customer table and inserts the sample customer records.

The generated database is stored under the SQLite data directory.

---

## 6. Data Source Implementation

### Step 6: Configure the CSV source

The CSV source contains eight sample customer records.

It includes customer ID, full name, email address, city, and customer creation date.

The extraction module reads the file into a pandas DataFrame.

### Step 7: Configure the SQLite source

The local SQLite source database contains five customer records.

Its table uses source-specific field names, including `customer_name`, `country`, and `registration_date`.

The extraction module executes a SQL query and loads the results into a pandas DataFrame.

### Step 8: Configure the REST API source

The project uses the JSONPlaceholder public users endpoint.

The extraction module sends an HTTP GET request, checks the HTTP response, parses the JSON response, and converts the returned records into a pandas DataFrame.

The API returns ten user records.

The API response contains nested address information. The extraction process normalizes nested JSON fields so that the city can be accessed as a regular DataFrame column.

### Step 9: Configure the webhook simulator

The webhook application is implemented using FastAPI.

It provides:

- A health endpoint.
- A POST endpoint to receive customer events.
- A GET endpoint to retrieve received events.

The POST endpoint validates the incoming event, adds source and ingestion-time metadata, and stores the event in an in-memory collection.

The current simulator is intentionally simple. Received events are lost when the FastAPI process restarts because they are not persisted to a database or durable message broker.

---

## 7. Standardization and Consolidation

### Step 10: Standardize the source records

The standardization module maps the four source-specific structures to a common set of fields.

The standardized schema is:

| Column        | Description                                             |
| ------------- | ------------------------------------------------------- |
| `source_id`   | Original identifier from the source system              |
| `full_name`   | Customer or user name                                   |
| `email`       | Email address                                           |
| `location`    | City or country value supplied by the source            |
| `created_at`  | Customer creation or registration date, when available  |
| `source`      | Name of the originating source                          |
| `ingested_at` | Timestamp at which the pipeline standardized the record |

The pipeline also creates a unique source-qualified `record_id`. For example, a CSV record with source ID `C001` becomes `csv_C001`.

Timestamps are converted to UTC-aware datetime values. Invalid or unavailable dates are represented as missing datetime values rather than fabricated.

**Known source differences:**

- The REST API does not provide a customer registration date, so its `created_at` values are missing.
- The SQLite source provides a country, while the other sources provide city-level locations. The current common `location` field therefore has mixed geographic granularity.

### Step 11: Consolidate the records

The standardized DataFrames are combined into one unified pandas DataFrame.

The resulting dataset includes a `source` field so that records can be traced to their original systems.

### Step 12: Validate data quality

The pipeline currently checks:

- Total record count.
- Duplicate record IDs.
- Missing email addresses.
- Missing customer names.
- Missing locations.

Duplicate record IDs cause the pipeline to stop before loading the staging repository.

---

## 8. Load the Unified Staging Repository

### Step 13: Load standardized data

The staging loader creates the staging directory when necessary and loads the unified DataFrame into a SQLite database.

**Staging database:** `data/staging/staging.db`

**Staging table:** `unified_customers`

The current implementation uses a full refresh. Each successful pipeline execution replaces the existing staging table with the latest consolidated dataset.

This makes repeated development runs predictable, but it is not an incremental or historical ingestion design.

---

## 9. Running the Project

### Step 14: Start the webhook server

Open a terminal in the project root, activate the virtual environment, and start the FastAPI application through Uvicorn.

Keep this terminal running while testing webhook ingestion.

The interactive API documentation is available at the local Swagger documentation endpoint on port 8000.

### Step 15: Submit a webhook event

Use the interactive API documentation to send a POST request to the customer webhook endpoint.

Provide a valid customer ID, full name, email, city, and creation date.

After submitting the event, retrieve the event list using the webhook GET endpoint. Confirm that the event appears in the response.

**Important:** The webhook event collection is held in memory. If the server restarts, submit the test event again before running the ingestion pipeline.

### Step 16: Run the unified ingestion pipeline

Open a second terminal in the project root, activate the virtual environment, and run the main ingestion application.

The pipeline extracts all four sources, standardizes the records, consolidates them, performs validation, and loads the staging table.

### Step 17: Verify the staging repository

Verify the record count and source-wise distribution in the `unified_customers` table.

The expected result for the current sample data is 24 records, distributed as follows:

- CSV: 8
- SQLite: 5
- REST API: 10
- Webhook: 1

---

## 10. Automated Testing

The project uses pytest.

The test suite is located in the `tests` directory.

It covers:

- Standardization of CSV records.
- Standardization of SQLite records.
- Standardization of REST API records.
- Standardization of webhook events.
- Conversion of source IDs to strings.
- Handling of unavailable or invalid dates.
- Rejection of unsupported source names.
- Consolidation of records from all four sources.
- Creation of source-qualified record IDs.
- Passing the unified DataFrame to the staging loader.
- Rejection of duplicate record IDs before loading.

The pipeline tests replace the external extractors and staging loader with controlled test doubles. They therefore do not require a live public API, a running webhook server, or a real staging database.

Run the test suite from the project root using pytest. A successful run should report all tests passing.

---

## 11. Project Folder Structure

```text
multi-source-data-ingestion/
│
├── .venv/
│
├── data/
│   ├── csv/
│   │   └── customers.csv
│   │
│   ├── sqlite/
│   │   ├── create_source_db.py
│   │   └── source.db
│   │
│   └── staging/
│       └── staging.db
│
├── docs/
│
├── src/
│   ├── sources/
│   │   ├── csv_source.py
│   │   ├── sqlite_source.py
│   │   ├── api_source.py
│   │   └── webhook_source.py
│   │
│   ├── transformations/
│   │   └── standardize.py
│   │
│   ├── loaders/
│   │   └── staging_loader.py
│   │
│   └── main.py
│
├── webhook/
│   └── app.py
│
├── tests/
│   ├── conftest.py
│   ├── test_standardize.py
│   └── test_ingestion.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

The `.venv` directory and generated database files are local development artifacts. Their inclusion in version control should follow the project's `.gitignore` policy.

---

## 12. Latest Execution and Validation Results

The latest successful execution produced the following results:

| Validation           | Result |
| -------------------- | -----: |
| CSV records          |      8 |
| SQLite records       |      5 |
| REST API records     |     10 |
| Webhook events       |      1 |
| Total extracted      |     24 |
| Total loaded         |     24 |
| Duplicate record IDs |      0 |
| Missing emails       |      0 |
| Missing names        |      0 |
| Missing locations    |      0 |

**Pipeline result:** SUCCESS

These results represent the latest observed execution. They are not a guarantee that every future run will produce the same counts, because the webhook event list is in memory and the API is external.

---

## 13. Known Limitations

1. **Webhook persistence:** Events are held in memory and disappear when the webhook server restarts.
2. **Full-refresh loading:** The staging loader replaces the table on every run; it does not implement incremental loading or deduplication across runs.
3. **API date availability:** The public API does not provide a customer registration date for the selected records.
4. **Location consistency:** The standardized location field mixes city-level and country-level values.
5. **External API dependency:** REST API extraction depends on network availability and the external service.
6. **Basic validation:** The current checks cover duplicates and missing key fields but do not implement a complete data-quality framework.
7. **Event processing:** The webhook simulator is not a durable message queue and does not provide retries, acknowledgements, or dead-letter handling.

---

## 15. Future Improvements

Possible extensions beyond the assignment include:

- Persist webhook events in SQLite instead of memory.
- Introduce a real message broker such as RabbitMQ or Kafka.
- Add incremental ingestion and idempotent loading.
- Add structured logging and retry mechanisms.
- Introduce schema validation and more comprehensive data-quality rules.
- Add source-level monitoring and ingestion metrics.
- Move the staging repository to PostgreSQL or a cloud data warehouse.

---

## 16. Conclusion

This project demonstrates a foundational multi-source data-ingestion workflow. It integrates file-based, relational database, REST API, and webhook-based sources into one standardized staging repository.

It also demonstrates the distinction between pull-based data extraction and push-based event delivery, along with basic data-quality validation and automated testing.

The implementation provides a foundation for more advanced ETL/ELT pipelines and analytics engineering workflows.
