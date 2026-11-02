import requests
import logging


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_coordinates(city):
    geocoding_response = requests.get(GEOCODING_URL, params={"name": city, "count": 1}, timeout=10)
    geocoding_response.raise_for_status()  # Raises HTTPError for unsuccessful HTTP responses.
    geocoding_data = geocoding_response.json()

    # Raise ValueError if the geocoding API returns no matching locations.
    if not geocoding_data.get("results"):
        raise ValueError("Invalid city. No data found.")

    latitude = geocoding_data["results"][0]["latitude"]
    longitude = geocoding_data["results"][0]["longitude"]

    return latitude, longitude, geocoding_data


def fetch_weather_data(latitude, longitude):
    # Parameters used to request weather data for the specified coordinates.
    params = {
    "latitude": latitude,
    "longitude": longitude,
    "current_weather": True
    }

    logging.info("Fetching weather data...")

    response = requests.get(WEATHER_URL, params=params, timeout=10)
    response.raise_for_status()  # Raises HTTPError for unsuccessful HTTP responses.

    logging.info("Weather data retrieved successfully")

    return response.json()