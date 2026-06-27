# Weather Pipeline

A simple data pipeline project that fetches weather data from a public API and stores it in a PostgreSQL database.

## Features

- Fetches current weather data from an API
- Extracts the fields needed for analysis
- Loads the data into PostgreSQL using psycopg2
- Can be run repeatedly to collect weather data over time
- Automated scheduling using Linux cron (runs hourly)

## Tech Stack

- Python
- PostgreSQL
- psycopg2
- Requests

## Setup

- Clone the repository.
  `git clone <repository-url>`
  `cd weather_pipeline`

## Create and activate a virtual environment.

`python -m venv .venv`
`source .venv/bin/activate` # Linux/macOS

## On Windows:

`.venv\Scripts\activate`

- Install the dependencies.
  `pip install -r requirements.txt`
- Create a PostgreSQL database and update your database credentials in the project.
- Run the pipeline.
  `python main.py`

## Example Data

The pipeline stores weather information such as:

- Temperature
- Wind speed
- Timestamp

## Future Improvements

- Docker support
- Environment variables for configuration
- Scheduled runs using cron (Now completed)
- Data validation and error handling
