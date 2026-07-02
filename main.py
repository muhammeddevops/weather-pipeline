import logging
from dotenv import load_dotenv
from datetime import datetime

from api import get_coordinates, extract
from transform import transform_geo_data, transform_weather_data
from storage import upload_raw_to_blob, container
from database import (
    get_connection,
    create_table,
    insert_weather_to_db,
    close_connection
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    user_input = input('Enter a city: ').strip()
    filename = 'weather' + datetime.now().strftime("%Y-%m-%d-%H-%M.json")
    
    # Extract
    latitude, longitude, geo_data = get_coordinates(user_input)
    weather_data = extract(latitude, longitude)
    
    # Transform
    temp, wind = transform_weather_data(weather_data)
    city, country = transform_geo_data(geo_data)
    
    # Load to Azure Blob
    upload_raw_to_blob(container, filename, weather_data)

    # Load to PostgreSQL
    conn = get_connection()

    try:
        create_table(conn)
        insert_weather_to_db(conn, city, country, temperature=temp, windspeed=wind)
    finally:
        close_connection(conn)

    print(f"In {city}, {country}")
    print(f"The temperature is currently {temp}")
    print(f"The wind speed is currently {wind}")
    print("Data inserted successfully")

if __name__ == "__main__":
    main()