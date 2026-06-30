import requests
import psycopg2
import json
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

user_input = input('Enter a city: ').strip()

url = "https://api.open-meteo.com/v1/forecast"
geo_url = "https://geocoding-api.open-meteo.com/v1/search"

geo_response = requests.get(geo_url, params={"name": user_input, "count": 1}, timeout=10)

geo_response.raise_for_status()  # Raises an exception if the status isn't 200-series

geo_data = geo_response.json()

if not geo_data.get("results"):
    raise ValueError("Invalid city. No data found.")


city = geo_data['results'][0]['name']
country = geo_data['results'][0]['country']

latitude = geo_data["results"][0]["latitude"]
longitude = geo_data["results"][0]["longitude"]

params = {
    "latitude": latitude,
    "longitude": longitude,
    "current_weather": True
}

response = requests.get(url, params=params, timeout=10)

response.raise_for_status()  # Raises an exception if the status isn't 200-series

weather_data = response.json()

temperature = weather_data['current_weather']['temperature']
windspeed = weather_data['current_weather']['windspeed']

filename = 'weather' + datetime.now().strftime("%Y-%m-%d-%H-%M.json")

connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

blob_service = BlobServiceClient.from_connection_string(connection_string)

container = blob_service.get_container_client('weathercontainer')

blob = container.get_blob_client(filename)


with open(filename, "w") as file:
    json.dump(weather_data, file, indent=4)

with open(filename, 'rb') as file:
    blob.upload_blob(file, overwrite=True)

print(f"In {city}, {country}")
print('The temperature is currently ', temperature)
print('And the wind speed is currently ', windspeed)

conn = psycopg2.connect(
    database='weather_project',
    user='postgres',
    password='newpassword123',
    host='localhost',
    port='5432'
)

cursor = conn.cursor()

#cursor.execute("DROP TABLE weather_data")
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        city CHAR(50),
        country CHAR(50),
        temperature FLOAT,
        windspeed FLOAT
    );
"""
)

cursor.execute(
    """
    INSERT INTO weather_data
    (city, country, temperature, windspeed)
    VALUES (%s, %s, %s, %s)
    """,
    (city, country, temperature, windspeed)
)

conn.commit()
cursor.close()
conn.close()

print('Data inserted succesfully')