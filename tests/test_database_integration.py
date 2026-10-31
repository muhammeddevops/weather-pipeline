from dotenv import load_dotenv

from database import get_connection, create_table, insert_weather_to_db

def test_insert_weather_to_postgres(monkeypatch):
    # Arrange
    load_dotenv()

    monkeypatch.setenv('DB_DATABASE', 'weather_project_test')
    monkeypatch.setenv('DB_HOST', 'localhost')
    monkeypatch.setenv('DB_PORT', '5433')

    conn = get_connection()

    city = 'Pytest Integration Test'
    country = 'United Kingdom'

    try:
        create_table(conn)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM weather_data WHERE city = %s AND country = %s",
            (city, country)
        )
        conn.commit()

        # Act
        insert_weather_to_db(conn, city, country, 15.5, 12.3)

        # Assert
        cursor.execute(
            """
            SELECT city, country, temperature, windspeed
            FROM weather_data
            WHERE city = %s AND country = %s
            ORDER BY id DESC
            LIMIT 1
            """,
            (city, country)
        )

        result = cursor.fetchone()

        assert result == (city, country, 15.5, 12.3)

    finally:
        cursor.execute(
            "DELETE FROM weather_data WHERE city = %s AND country = %s",
            (city, country)
        )
        conn.commit()
        cursor.close()
        conn.close()