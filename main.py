import logging
from dotenv import load_dotenv

import requests
from api import get_coordinates, fetch_weather_data
from transform import transform_geo_data, transform_weather_data
from database import (
    get_connection,
    create_table,
    insert_weather_to_db,
    close_connection
)
import psycopg2

# Load environment variables from the .env file
load_dotenv()

# Configure logging to display INFO-level messages and above, including timestamps and severity levels
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    user_input = input('Enter a city: ').strip()

    if not user_input:
        print("Please enter a city.")
        return
    
    # Extract
    try:
        # Retrieve geographic coordinates and the original geocoding response.
        latitude, longitude, geo_data = get_coordinates(user_input)
     
        weather_data = fetch_weather_data(latitude, longitude)

    # Handle cases where the geocoding API returns no matching location.
    except ValueError as error:
        logging.warning(f"Invalid city: {error}")
        print("City not found. Please check the city name.")
        return

    # Handle HTTP errors encountered when communicating with the APIs.
    except requests.exceptions.RequestException:
        logging.exception("Failed to retrieve data from weather API")
        print("Unable to retrieve weather data. Please try again later.")
        return
    
    # Transform
    temp, wind = transform_weather_data(weather_data)
    city, country = transform_geo_data(geo_data)
    
    # Initialise conn to None so the finally block can safely check whether a connection was established.
    conn = None 

    # Load the transformed weather data into PostgreSQL    
    try:
        conn = get_connection()
        create_table(conn)
        insert_weather_to_db(conn, city, country, temperature=temp, windspeed=wind)

    # Handle database errors during connection, table creation or data insertion.
    except psycopg2.Error:
        logging.exception("Database operation failed")
        print("Unable to save weather data to the database.")
        return

    finally:
        if conn is not None:
            close_connection(conn)

    print(f"\nWeather in {city}, {country}")
    print(f"Temperature: {temp}°C")
    print(f"Wind speed: {wind} km/h")
    print("\nData successfully saved to PostgreSQL")

# Execute main() only when this file is run directly, rather than imported as a module.
if __name__ == "__main__":
    main()