import psycopg2
import logging
import os


def get_connection():
    return psycopg2.connect(
    database=os.getenv("DB_DATABASE"),
    user=os.getenv('DB_USER'),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432")
    )

def create_table(conn):
    cursor = conn.cursor()

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        city VARCHAR(50),
        country VARCHAR(50),
        temperature FLOAT,
        windspeed FLOAT
    );
    """
    )
    conn.commit()

    cursor.close()
    

def insert_weather_to_db(conn, city, country, temperature, windspeed):
    cursor = conn.cursor()

    query = """
    INSERT INTO weather_data
    (city, country, temperature, windspeed)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (city, country, temperature, windspeed)
        )
    conn.commit()    
    logging.info("Successfully inserted row into PostgeSQL")
    cursor.close()

def close_connection(conn):
    conn.close()
    
def drop_table(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE weather_data")