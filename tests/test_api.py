import pytest
import requests
from unittest.mock import Mock, patch

from api import get_coordinates, extract

@patch("api.requests.get")
def test_get_coordinates_success(mock_get):
    #Arrange: Set up the mock response and define the data it should return
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": [
            {
                "name": "Manchester",
                "country": "United Kingdom",
                "latitude": 53.48,
                "longitude": -2.24
            }
        ]
    }
    mock_get.return_value = mock_response

    #Act: Call get_coordinates and save the result to latitude, longitude and geo_data
    latitude, longitude, geo_data = get_coordinates("Manchester")

    #Assert: Check that the returned data contains the expected values
    assert latitude == 53.48
    assert longitude == -2.24
    assert geo_data["results"][0]["name"] == "Manchester"
    mock_get.assert_called_once()

@patch("api.requests.get")
def test_extract_success(mock_get):
    #Arrange: Set up the mock response and define the data it should return
    mock_response = Mock()
    mock_response.json.return_value = {
        "current_weather": {
            "temperature": 15.5,
            "windspeed": 12.3
        }
    }
    mock_get.return_value = mock_response

    #Act: Call extract() with the test coordinates and assign it to result 
    result = extract(53.48, -2.24)

    #Assert: Check that the returned data contains the expected values
    assert result["current_weather"]["temperature"] == 15.5
    assert result["current_weather"]["windspeed"] == 12.3
    mock_get.assert_called_once()


@patch("api.requests.get")
def test_extract_api_error(mock_get):
    #Arrange: Set up a mock response that raises a HTTPError
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError("API error")
    )
    mock_get.return_value = mock_response

    #Act and Assert: Call extract() and check that it raises a HTTPError
    with pytest.raises(requests.exceptions.HTTPError):
        extract(53.48, -2.24)