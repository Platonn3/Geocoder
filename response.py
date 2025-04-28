import requests


def get_full_address(address):
    headers = {
        "User-Agent": "MyGeocoderApp/1.0 (platon.kurbatov87@gmail.com)"
    }
    params = {'q': address,
              'format': 'json',
              "limit": 1,
              "accept-language": "ru"
              }
    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params=params,
        headers=headers,
        timeout=10
    )
    if response.ok:
        if response.text.strip():
            data = response.json()
            if data:
                print(data[0])
