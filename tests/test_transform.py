from transform import transform_geo_data, transform_weather_data
import pytest


def test_transform_geo_data():
    #Arrange: Set up the test data
    geo_data = {
        "results": [
            {
                "name": "Manchester",
                "country": "United Kingdom"
            }
        ]
    }
    #Act: Run the function and store the result
    result = transform_geo_data(geo_data)

    #Assert: Assert that the result is as expected
    assert result == ("Manchester", "United Kingdom")


def test_transform_weather_data():
    weather_data = {
        "current_weather": {
            "temperature": 15.5,
            "windspeed": 12.3
        }
    }

    result = transform_weather_data(weather_data)

    assert result == (15.5, 12.3)


def test_transform_weather_data_missing_windspeed():
    weather_data = {
        "current_weather": {
            "temperature": 15.5
        }
    }

    with pytest.raises(KeyError):
        transform_weather_data(weather_data)