from flask import Flask
import os
import requests

key = os.getenv('WEATHER_KEY', 'no_value')

app = Flask(__name__)

list_cities = ['Lisbon,PT', 'Porto,PT', 'London,GB', 'Munich,DE', 'Paris,FR']
cities = {}
for city in list_cities:
    coordinates = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={key}')
    cities[city[:-3]] = (coordinates.json()[0]['lat'], coordinates.json()[0]['lon'])


@app.route('/')
def index():
    return 'Hello World!' if key != 'no_value' else 'weather key has no value'


@app.route('/weather/current/<city>')
def get_current_temperature(city):

    lat = cities[city][0]
    lon = cities[city][1]

    exclude = 'minutely,hourly,daily,alerts'
    weather = requests.get(
        f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={key}&units=metric')

    temperature = {}
    temperature['unit'] = 'Celsius (°C)'
    temperature['current'] = weather.json()['current']['temp']
    temperature['feels_like'] = weather.json()['current']['feels_like']

    return temperature

# @app.route('/weather/stats/<city>')
# def get_temperature_status(city):
#     lat = cities[city][0]
#     lon = cities[city][1]

#     exclude = 'current,minutely,hourly,alerts'
#     weather = requests.get(
#         f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={key}&units=metric')

#     return weather.json()

if __name__ == "__main__":
    app.run()
