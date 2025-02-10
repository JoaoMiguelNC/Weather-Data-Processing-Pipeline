import requests

url = 'https://weather-api-724625757672.europe-west1.run.app/weather/current/{city}'


class TestAPI():

    def test_lisbon_01(self):
        answer = requests.get(url.format(city='Lisbon,PT')).status_code
        assert answer == 200

    def test_lisbon_02(self):
        answer = len(requests.get(url.format(city='Lisbon,PT')).json())
        assert answer == 1

    def test_lisbon_03(self):
        answer = len(requests.get(url.format(city='Lisbon,PT')).json()[0])
        assert answer == 4

    def test_lisbon_04(self):
        answer = requests.get(url.format(city='Lisbon,PT')).json()[0]
        assert answer['country'] == 'PT'
        assert answer['name'] == 'Lisbon'
        assert answer['unit'] == 'Celsius (°C)'