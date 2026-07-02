from dotenv import load_dotenv
from datetime import datetime
from api import get_coordinates, extract
from transform import transform_geo_data, transform_weather_data
from storage import upload_raw_to_blob, container
from database import get_connection, create_table, insert_weather_to_db, close_connection

load_dotenv()    

user_input = input('Enter a city: ').strip()
filename = 'weather' + datetime.now().strftime("%Y-%m-%d-%H-%M.json")
#
latitude, longitude, geo_data = get_coordinates(user_input)
weather_data = extract(latitude, longitude)
#
temp, wind = transform_weather_data(weather_data)
city, country = transform_geo_data(geo_data)
#
upload_raw_to_blob(container, filename, weather_data)

#
conn = get_connection()
create_table(conn)
insert_weather_to_db(conn, city, country, temperature=temp, windspeed=wind)
close_connection(conn)


print(f"In {city}, {country}")
print('The temperature is currently ', temp)
print('And the wind speed is currently ', wind)

print('Data inserted succesfully')