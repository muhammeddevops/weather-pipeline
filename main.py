import logging
from dotenv import load_dotenv

import requests
from api import get_coordinates, extract
from transform import transform_geo_data, transform_weather_data
from database import (
    get_connection,
    create_table,
    insert_weather_to_db,
    close_connection
)
import psycopg2

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    user_input = input('Enter a city: ').strip()
    
    # Extract
    try:
        latitude, longitude, geo_data = get_coordinates(user_input)
        weather_data = extract(latitude, longitude)

    except ValueError as error:
        logging.warning(f"Invalid city: {error}")
        print("City not found. Please check the city name.")
        return

    except requests.exceptions.RequestException:
        logging.exception("Failed to retrieve data from weather API")
        print("Unable to retrieve weather data. Please try again later.")
        return
    
    # Transform
    temp, wind = transform_weather_data(weather_data)
    city, country = transform_geo_data(geo_data)
    
    # Set connection as none so that if get_connection() fails close_connection() will not be called
    conn = None 

    # Load to PostgreSQL    
    try:
        conn = get_connection()
        create_table(conn)
        insert_weather_to_db(conn, city, country, temperature=temp, windspeed=wind)

    except psycopg2.Error:
        logging.exception("Database operation failed")
        print("Unable to save weather data to the database.")
        return
    
    finally:
        if conn is not None:
            close_connection(conn)

    print(f"In {city}, {country}")
    print(f"The temperature is currently {temp}")
    print(f"The wind speed is currently {wind}")
    print("Data inserted successfully")

# Only runs main() if this file is the starting point, not if it's being imported elsewhere.
if __name__ == "__main__":
    main()