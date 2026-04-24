from unittest.mock import patch

import requests


def get_current_weather(city='Tbilisi'):
    api_key = '5401f3fc2046e2993c67ed01d4165add'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    response = requests.get(url, params={
        'q': city,
        'appid': api_key,
        'units': 'metric'
    })
    result: dict = response.json()
    return f'{result['main']['temp']}°, {result['weather'][0]['description']}'


@patch('requests.get')
def test_get_current_weather(mock_get):
    # requests.get().json()

    mock_get.return_value.json.return_value = {
        'main': {'temp': 20},
        'weather': [{'description': 'sunny'}]
    }
    assert get_current_weather() == '20°, sunny'
    mock_get.assert_called_once_with(
        'https://api.openweathermap.org/data/2.5/weather', params={
            'q': 'Tbilisi',
            'appid': '5401f3fc2046e2993c67ed01d4165add',
            'units': 'metric'
        })
    mock_get.assert_called()
