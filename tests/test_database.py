
from unittest.mock import Mock, patch

from database import (
    get_connection,
    create_table,
    insert_weather_to_db,
    close_connection
)


def test_get_connection(monkeypatch):
    # Arrange: Set up environment variables
    monkeypatch.setenv("DB_DATABASE", "weather_project")
    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.setenv("DB_PASSWORD", "test_password")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")

    # Act: Mock the database connection
    with patch("database.psycopg2.connect") as mock_connect:
        expected_connection = Mock()
        mock_connect.return_value = expected_connection

        result = get_connection()

    # Assert
    assert result == expected_connection
    mock_connect.assert_called_once_with(
        database="weather_project",
        user="postgres",
        password="test_password",
        host="localhost",
        port="5432"
    )


def test_create_table():
    # Arrange
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor

    # Act
    create_table(mock_conn)

    # Assert
    sql = mock_cursor.execute.call_args[0][0]

    assert "CREATE TABLE IF NOT EXISTS weather_data" in sql
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


def test_insert_weather_to_db():
    # Arrange
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor

    # Act
    insert_weather_to_db(
        mock_conn,
        "Manchester",
        "United Kingdom",
        15.5,
        12.3
    )

    # Assert
    sql, values = mock_cursor.execute.call_args[0]

    assert "INSERT INTO weather_data" in sql
    assert values == ("Manchester", "United Kingdom", 15.5, 12.3)
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()


def test_close_connection():
    # Arrange
    mock_conn = Mock()

    # Act
    close_connection(mock_conn)

    # Assert
    mock_conn.close.assert_called_once()