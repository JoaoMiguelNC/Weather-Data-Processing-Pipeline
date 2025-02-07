import requests

with open('key.txt') as f:
    key = f.read()

    city = 'Lisbon'
    country = 'PT'

coordinates = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit=1&appid={key}')

lat = coordinates.json()[0]['lat']
lon = coordinates.json()[0]['lon']

weather = requests.get(f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={key}&units=metric')

for x in weather.json():
    print(x)

print()
print(weather.json())