from flask import Flask
import os
import requests

key = os.getenv('WEATHER_KEY')

app = Flask(__name__)


def get_coordinates_response(city):
    response = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=10&appid={key}')

    return response.status_code, response.json()


def get_coordinates(response):

    cities = []
    for city in response:
        cities.append({
            'name': city['name'],
            'country': city['country'],
            'state': city.get('state'),
            'lat': city['lat'],
            'lon': city['lon'],
        })

    return cities


def get_current_temperature(response):

    cities = get_coordinates(response)
    cities_weather = []

    exclude = 'minutely,hourly,daily,alerts'
    for c in cities:
        weather = requests.get(
            f"https://api.openweathermap.org/data/3.0/onecall?lat={c['lat']}&lon={c['lon']}&exclude={exclude}&appid={key}&units=metric"
        ).json()

        cities_weather.append({
            'name': c['name'],
            'country': c['country'],
            'temperature': weather['current']['temp'],
            'unit': 'Celsius (°C)',
        } | ({'state': c['state']} if c.get('state') else {}))

    return cities_weather


@app.route('/')
def index():

    status, response = get_coordinates_response('lisbon')

    return get_current_temperature(response) if status == 200 and response else f'ERROR: city is not a valid city!'


@app.route('/weather/current/<city>')
def current_temperature(city):

    status, response = get_coordinates_response(city)

    return get_current_temperature(response) if status == 200 and response else f'ERROR: {city} is not a valid city!'

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
