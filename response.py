import requests
import parsing as parse


def send_request(address):
    headers = {
        "User-Agent": "MyGeocoderApp/1.0 (platon.kurbatov87@gmail.com)"
    }
    params = {"q": address,
              "format": "json",
              "limit": 1,
              "accept-language": "ru"
              }
    try:
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
                    address = data[0]
                    parse.parse_output_address(address)
                else:
                    print("Адрес не найден")
            else:
                print("Пустой ответ от сервера")
        else:
            print(f"Ошибка HTTP: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса {e}")

