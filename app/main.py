from flask import Flask
import os
import requests

from google.cloud.secretmanager import SecretManagerServiceClient, AccessSecretVersionRequest

# Getting OpenWeatherMap key from Secret manager
secret_client: SecretManagerServiceClient = SecretManagerServiceClient()
secret_request: AccessSecretVersionRequest = AccessSecretVersionRequest(
    name='open-weather-map-key ')
key = secret_client.access_secret_version(
    request=secret_request).payload.data.decode('utf-8')


app = Flask(__name__)

list_cities = ['Lisbon']


@app.route('/')
def index():
    return 'Hello!'


@app.route('/weather/current/<city>')
def get_current_temperature(city):
    coordinates = requests.get(
        f'http://api.openweathermap.org/geo/1.0/direct?q={city},PT&limit=1&appid={key}')

    lat = coordinates.json()[0]['lat']
    lon = coordinates.json()[0]['lon']

    exclude = 'minutely,hourly,daily,alerts'
    weather = requests.get(
        f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={key}&units=metric')

    temperature = {}
    temperature['unit'] = 'Celsius (°C)'
    temperature['current'] = weather.json()['current']['temp']
    temperature['feels_like'] = weather.json()['current']['feels_like']

    return temperature

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))