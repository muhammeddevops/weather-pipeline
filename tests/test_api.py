import pytest
import requests
from unittest.mock import Mock, patch

from api import get_coordinates, extract

@patch("api.requests.get")
def test_get_coordinates_success(mock_get):
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
   
    latitude, longitude, geo_data = get_coordinates("Manchester")

    assert latitude == 53.48
    assert longitude == -2.24
    assert geo_data["results"][0]["name"] == "Manchester"
    mock_get.assert_called_once()

@patch("api.requests.get")
def test_extract_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "current_weather": {
            "temperature": 15.5,
            "windspeed": 12.3
        }
    }
    mock_get.return_value = mock_response

    result = extract(53.48, -2.24)

    assert result["current_weather"]["temperature"] == 15.5
    assert result["current_weather"]["windspeed"] == 12.3
    mock_get.assert_called_once()


@patch("api.requests.get")
def test_extract_api_error(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError("API error")
    )
    mock_get.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        extract(53.48, -2.24)