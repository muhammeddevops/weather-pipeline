import requests
import psycopg2

url = "https://api.open-meteo.com/v1/forecast"

city = input('Enter a city:')

geo_url = "https://geocoding-api.open-meteo.com/v1/search"

geo_response = requests.get(geo_url, params={"name": city, "count": 1})

geo_data = geo_response.json()

latitude = geo_data["results"][0]["latitude"]
longitude = geo_data["results"][0]["longitude"]

params = {
    "latitude": latitude,
    "longitude": longitude,
    "current_weather": True
}



response = requests.get(url, params=params)

data = response.json()

temperature = data['current_weather']['temperature']
windspeed = data['current_weather']['windspeed']

print('The temperature is currently ', temperature)
print('And the wind speed is currently ', windspeed)

connection_uri = "postgresql+psycopg2://postgres:newpassword123@localhost:5432/weather_project"


conn = psycopg2.connect(
    database='weather_project',
    user='postgres',
    password='newpassword123',
    host='localhost',
    port='5432'
)

cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        city CHAR(50),
        temperature FLOAT,
        windspeed FLOAT
    );
"""
)

cursor.execute(
    """
    INSERT INTO weather_data
    (city, temperature, windspeed)
    VALUES (%s, %s, %s)
    """,
    (city, temperature, windspeed)
)

conn.commit()


print('Data inserted succesfully')    