import requests
import sqlite3
from yr.libyr import Yr
import json
import re

conn = sqlite3.connect("yr_database.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS weather (Place text,"
               "Weather_description text, Precipitation text,"
               "Wind_direction text, Wind_direction_code text, Wind_speed text,"
               "Wind_speed_description text, Temperature_text,"
               "Pressure_text)")

list = ["Portugal/Coimbra/Coimbra/", "Portugal/Porto/Porto/", "Portugal/Lisboa/Lisboa/", "Portugal/Leiria/Nazare/"]

for place in list:
    for i in place:
        weather = Yr(location_name=place, forecast_link='forecast_hour_by_hour')

        forecast = weather.forecast(as_json=True).__next__()
        data = json.loads(forecast)
        dict = {}
        dict["Place"] = re.sub(r'[^\w]', ' ', place)
        dict["Weather description"] = data["symbol"]["@name"]
        dict["Precipitation"] = data["precipitation"]["@value"]
        dict["Wind direction"] = data["windDirection"]["@name"]
        dict["Wind direction code"] = data["windDirection"]["@code"]
        dict["Wind speed"] = data["windSpeed"]["@mps"]
        dict["Wind speed description"] = data["windSpeed"]["@name"]
        dict["Temperature"] = data["temperature"]["@value"] + " " + data["temperature"]["@unit"]
        dict["Pressure"] = data["pressure"]["@value"] + " " + data["pressure"]["@unit"]

    list_to_add = dict["Place"], dict["Weather description"], \
                  dict["Precipitation"], dict["Wind direction"], \
                  dict["Wind direction code"], dict["Wind speed"], \
                  dict["Wind speed description"], dict["Temperature"], \
                  dict["Pressure"]

    cursor.execute("INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", list_to_add)

conn.commit()
cursor.close()
conn.close()
