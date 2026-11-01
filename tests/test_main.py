from unittest.mock import Mock, patch
import psycopg2
import main
import requests
import runpy


def test_main_success(capsys):
    # Arrange
    geo_data = {
        "results": [
            {
                "name": "Manchester",
                "country": "United Kingdom"
            }
        ]
    }

    weather_data = {
        "current_weather": {
            "temperature": 15.5,
            "windspeed": 12.3
        }
    }

    mock_conn = Mock()

    with patch("builtins.input", return_value=" Manchester "), \
         patch("main.get_coordinates") as mock_coordinates, \
         patch("main.extract") as mock_extract, \
         patch("main.transform_weather_data") as mock_transform_weather, \
         patch("main.transform_geo_data") as mock_transform_geo, \
         patch("main.get_connection", return_value=mock_conn), \
         patch("main.create_table") as mock_create_table, \
         patch("main.insert_weather_to_db") as mock_insert, \
         patch("main.close_connection") as mock_close:

        mock_coordinates.return_value = (53.48, -2.24, geo_data)
        mock_extract.return_value = weather_data
        mock_transform_weather.return_value = (15.5, 12.3)
        mock_transform_geo.return_value = ("Manchester", "United Kingdom")

        # Act
        main.main()

        # Assert
        mock_coordinates.assert_called_once_with("Manchester")
        mock_extract.assert_called_once_with(53.48, -2.24)

        mock_transform_weather.assert_called_once_with(weather_data)
        mock_transform_geo.assert_called_once_with(geo_data)

        mock_create_table.assert_called_once_with(mock_conn)

        mock_insert.assert_called_once_with(
            mock_conn,
            "Manchester",
            "United Kingdom",
            temperature=15.5,
            windspeed=12.3
        )

        mock_close.assert_called_once_with(mock_conn)

    output = capsys.readouterr().out

    assert "In Manchester, United Kingdom" in output
    assert "The temperature is currently 15.5" in output
    assert "The wind speed is currently 12.3" in output
    assert "Data inserted successfully" in output


def test_main_database_connection_error(capsys):
    # Arrange
    mock_conn = Mock()

    with (
        patch("builtins.input", return_value="Manchester"),
        patch("main.get_coordinates", return_value=(53.48, -2.24, {})),
        patch("main.extract", return_value={}),
        patch("main.transform_weather_data", return_value=(15.5, 12.3)),
        patch("main.transform_geo_data", return_value=("Manchester", "United Kingdom")),
        patch("main.get_connection", return_value=mock_conn),
        patch("main.create_table"),
        patch("main.insert_weather_to_db", side_effect=psycopg2.Error),
        patch("main.close_connection") as mock_close
    ):
        # Act
        main.main() 

    # Assert
    output = capsys.readouterr().out

    assert "Unable to save weather data to the database." in output
    mock_close.assert_called_once_with(mock_conn)


def test_main_invalid_city(capsys):
    # Arrange
    with (
        patch("builtins.input", return_value="InvalidCity"),
        patch("main.get_coordinates", side_effect=ValueError("Invalid city"))
    ):
        # Act
        main.main()

    # Assert
    output = capsys.readouterr().out
    assert "City not found. Please check the city name." in output


def test_main_api_error(capsys):
    # Arrange
    with (
        patch("builtins.input", return_value="Manchester"),
        patch("main.get_coordinates", return_value=(53.48, -2.24, {})),
        patch("main.extract", side_effect=requests.exceptions.RequestException)
    ):
        # Act
        main.main()

    # Assert
    output = capsys.readouterr().out
    assert "Unable to retrieve weather data. Please try again later." in output