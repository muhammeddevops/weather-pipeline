import psycopg2
import logging
import os

def get_connection():
    """Establish and return a connection to the PostgreSQL database."""   
    return psycopg2.connect(
    database=os.getenv("DB_DATABASE"),
    user=os.getenv('DB_USER'),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432")
    )

def create_table(conn):
    """Create the weather_data table if it does not already exist."""
    
    with conn.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weather_data (
                id SERIAL PRIMARY KEY,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                city VARCHAR(100) NOT NULL,
                country VARCHAR(100) NOT NULL,
                temperature DOUBLE PRECISION,
                windspeed DOUBLE PRECISION
            );
            """
        )
    conn.commit()
    
def insert_weather_to_db(conn, city, country, temperature, windspeed):
    """Insert the transformed weather and location data into PostgreSQL."""

    query = """
            INSERT INTO weather_data
            (city, country, temperature, windspeed)
            VALUES (%s, %s, %s, %s)
            """
    
    with conn.cursor() as cursor:

        cursor.execute(
            query,
            (city, country, temperature, windspeed)
        )
        
    conn.commit()    
    logging.info("Successfully inserted row into PostgreSQL")

def close_connection(conn):
    """Close the PostgreSQL database connection."""
    conn.close()

def drop_table(conn):
    """Permanently drop the weather_data table."""

    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS weather_data")

    conn.commit()