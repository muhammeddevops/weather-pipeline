import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

geo_url = "https://geocoding-api.open-meteo.com/v1/search"

def get_coordinates(city):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    
    geo_response = requests.get(geo_url, params={"name": city, "count": 1}, timeout=10)
    geo_response.raise_for_status()  # Raises an exception if the status isn't 200-series
    geo_data = geo_response.json()

    if not geo_data.get("results"):
        raise ValueError("Invalid city. No data found.")

    latitude = geo_data["results"][0]["latitude"]
    longitude = geo_data["results"][0]["longitude"]

    return latitude, longitude, geo_data


def extract(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
    "latitude": latitude,
    "longitude": longitude,
    "current_weather": True
    }
    try:
        logging.info("Fetching weather data...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raises an exception if the status isn't 200-series
        logging.info("Weather data retrieved succesfully")
        response.json()
    except:
        logging.error("Failed to connect to weather API.")
        raise
    return response.json()


