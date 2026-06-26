import requests
from sqlalchemy import create_engine, text
import psycopg2

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 53.48,
    "longitude": -2.24,
    "current_weather": True
}

response = requests.get(url, params=params)

data = response.json()

temperature = data['current_weather']['temperature']
windspeed = data['current_weather']['windspeed']

print('The temperature is currently ', temperature)
print('And the wind speed is currently ', windspeed)

connection_uri = "postgresql+psycopg2://postgres:newpassword123@localhost:5432/weather_project"

engine = create_engine(connection_uri)

"""
with engine.begin() as conn:
    conn.execute(text("DROP TABLE weather_data"))
"""


'''
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            temperature NUMERIC,
            windspeed NUMERIC     
    )
"""))
    
with engine.begin() as conn:
    conn.execute(text("""
        INSERT INTO weather_data (temperature, windspeed)
        VALUES (:temperature, :windspeed)
"""), {
    'temperature': temperature,
    'windspeed': windspeed
})
'''

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
        temperature float,
        windspeed float
    );
"""
)

cursor.execute(
    """
    INSERT INTO weather_data
    (temperature, windspeed)
    VALUES (%s, %s)
    """,
    (temperature, windspeed)
)

conn.commit()


print('Data inserted succesfully')    