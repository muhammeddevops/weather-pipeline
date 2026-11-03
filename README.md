# Weather Data Pipeline

A Python-based data pipeline that retrieves real-time weather data from the Open-Meteo API, transforms the response and stores the results in a PostgreSQL database.

The project was built to develop practical data engineering skills, focusing on API integration, data transformation, database management, containerisation and automated testing.

## Project Overview

The pipeline allows users to enter a city and retrieves its current weather information using the Open-Meteo Geocoding and Weather APIs.

The extracted data is then transformed into a structured format and loaded into a PostgreSQL database for storage.

### Pipeline Workflow

1. **Input:** The user enters a city name.
2. **Extract:** The Open-Meteo Geocoding API retrieves the city's geographical coordinates, which are used to request current weather data.
3. **Transform:** The API responses are processed to extract relevant information, including city, country, temperature and wind speed.
4. **Load:** The transformed data is inserted into a PostgreSQL database.

## Technologies Used

| Technology     | Purpose                                          |
| -------------- | ------------------------------------------------ |
| Python         | Core programming language                        |
| Open-Meteo API | Weather and geocoding data source                |
| PostgreSQL     | Relational database for storing weather records  |
| SQL            | Database queries and data manipulation           |
| Docker         | Application containerisation                     |
| Docker Compose | Managing the application and database containers |
| Pytest         | Unit and integration testing                     |
| Git & GitHub   | Version control                                  |

## Project Structure

```text
weather-pipeline/
│
├── api.py              # API requests and data extraction
├── transform.py        # Data transformation
├── database.py         # PostgreSQL connection and operations
├── main.py             # Main pipeline execution
│
├── tests/              # Unit and integration tests
│
├── Dockerfile          # Application container configuration
├── compose.yaml        # Docker Compose configuration
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Docker
- Docker Compose

### 1. Clone the repository

```bash
git clone <repository-url>
cd weather-pipeline
```

### 2. Configure environment variables

Create a `.env` file in the project root directory containing your PostgreSQL connection settings.

```env
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=weather_project
DB_USER=your_username
DB_PASSWORD=your_password
```

_Note: The application connects to PostgreSQL through the Docker Compose network using the service name `postgres` and the container port `5432`. The database is exposed on host port `5433`._

### 3. Start the application

Build and start the containers using Docker Compose:

```bash
docker compose up --build
```

### 4. Run the pipeline

When the application starts, enter a city name when prompted.

The pipeline will retrieve the weather data, transform the response and store the resulting record in PostgreSQL.

## Testing

The project uses Pytest for unit and integration testing.

Run the test suite:

```bash
python -m pytest -v
```

Run tests with a coverage report:

```bash
python -m pytest --cov=. --cov-report=term-missing
```

The tests cover API requests, data transformation, database operations and pipeline execution.

## Future Improvements

Potential areas for further development include:

- Automating scheduled data collection.
- Expanding the dataset to include historical weather information.
- Implementing data validation and quality checks.
- Improving pipeline monitoring and error handling.
- Exploring cloud-based data storage and processing.

## Data Source

Weather and geographical data are provided by the [Open-Meteo API](https://open-meteo.com/).
