def transform_geo_data(geo_data):
    city = geo_data['results'][0]['name']
    country = geo_data['results'][0]['country']
    return city, country

def transform_weather_data(weather_data):
    temperature = weather_data['current_weather']['temperature']
    windspeed = weather_data['current_weather']['windspeed']

    return temperature, windspeed