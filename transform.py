def transform_geo_data(geo_data):
    """Extract the city and country from the geocoding API response."""

    city = geo_data['results'][0]['name']
    country = geo_data['results'][0]['country']
    
    return city, country

def transform_weather_data(weather_data):
    """Extract the current temperature and wind speed from the weather API response."""

    temperature = weather_data['current_weather']['temperature']
    windspeed = weather_data['current_weather']['windspeed']

    return temperature, windspeed