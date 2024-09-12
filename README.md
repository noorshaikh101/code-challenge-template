# Code Challenge Template

## Weather Data Processing API
This project ingests weather data from multiple weather stations, processes and stores it in a database, and provides a REST API to retrieve the ingested and processed weather data. The data spans from 1985-01-01 to 2014-12-31 for stations located in Nebraska, Iowa, Illinois, Indiana, and Ohio.

## Problem 1 - Data Modeling
The weather data files contain the following records:

- Date in YYYYMMDD format.
- Maximum temperature in tenths of a degree Celsius.
- Minimum temperature in tenths of a degree Celsius.
- Precipitation in tenths of a millimeter.
- Missing values are indicated by -9999.


## Problem 2 - Ingestion
To ingest the weather data from the provided files, use the script located at:
 
``` /src/ingest_weather_data.py ```

Ingestion Process
Reads the weather data files from the wx_data directory.
Skips any data that is already present in the database (checks for duplicates).
Logs start and end times, and the number of records ingested.
To run the ingestion script:

``` python src/ingest_weather_data.py  ```

## Problem 2 - Ingestion
To ingest the weather data from the provided files, use the script located at:

```/src/ingest_weather_data.py```

Ingestion Process
Reads the weather data files from the wx_data directory.
Skips any data that is already present in the database (checks for duplicates).
Logs start and end times, and the number of records ingested.
To run the ingestion script:

``` python src/ingest_weather_data.py ```

## Problem 3 - Data Analysis
For every weather station and year, the following statistics are calculated:

Average Maximum Temperature (in degrees Celsius)
Average Minimum Temperature (in degrees Celsius)
Total Precipitation (in centimeters)
Missing values are ignored during calculations.

Script for Calculating Statistics
The script for calculating and storing weather statistics is located at:

``` /src/calculate_weather_stats.py ```

Run the script:

``` python src/calculate_weather_stats.py ```

## Problem 4 - REST API
The REST API provides access to the ingested and calculated weather data.

Endpoints
1. GET /api/weather

- Fetches raw weather data.
- Filters available via query parameters:
    - station_id: Filter by weather station ID.
    - date: Filter by specific date (YYYY-MM-DD).

2. GET /api/weather/stats

- Fetches calculated weather statistics.
- Filters available via query parameters:
    - station_id: Filter by weather station ID.
    - year: Filter by specific year.

## Response Format
Both endpoints return data in JSON format.
Responses are paginated, with 100 records per page by default

## API Documentation (Swagger/OpenAPI)
The API documentation is automatically generated using Swagger and can be accessed at:
/api/docs

The OpenAPI specification is located at:

/src/static/swagger.json

## Run the API
To run the API locally, use:

``` python src/app.py ```

The API will be available at http://localhost:5000/

## Deployment

### Cloud Deployment using AWS

To deploy the API, database, and ingestion system in the cloud, we would use the following AWS services:

1. Elastic Beanstalk: For deploying the Flask-based API.
2. Amazon RDS: For hosting the PostgreSQL database.
3. AWS Lambda: For running the ingestion code as a scheduled job.
4. Amazon CloudWatch: To trigger AWS Lambda at regular intervals (e.g., daily).
5. Amazon S3: To store raw weather data files (optional).

## Approach
1. API Deployment:

- Use Elastic Beanstalk to deploy the Flask app. It provides a managed environment, handling scaling, monitoring, and load balancing.

2. Database Deployment:

- Use Amazon RDS to set up a PostgreSQL instance for storing both raw weather data and statistics.

3. Ingestion Process:

- Deploy the ingestion script as an AWS Lambda function.
- Schedule the Lambda function using Amazon CloudWatch Events to run periodically (e.g., daily at midnight).
- Optionally, store the raw weather data files in Amazon S3 and use Lambda to read from S3 for ingestion.

4. Monitoring:

- Use Amazon CloudWatch Logs to monitor the API and ingestion process.

## Running the Project Locally

Step 1: Clone the Repository

```
    git clone https://github.com/noorshaikh101/code-challenge-template.git
    cd code-challenge-template
```

Step 2: Set Up a Virtual Environment

```
    python3 -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate  # For Windows
```

Step 3: Install Dependencies

```
pip install -r requirements.txt
```

Step 4: Set Up the Database

``` 
CREATE DATABASE weather_db;
```

Step 5: Run the API

```
python src/app.py
```

Step 6: Ingest Weather Data
```
To ingest the weather data into the database:
```
Step 7: Calculate Weather Statistics

```
python src/calculate_weather_stats.py
```
