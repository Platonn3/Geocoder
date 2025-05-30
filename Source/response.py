import requests
from Source import parsing as parse
from Source.database.requests import return_address_if_exist


async def send_request(address):
    headers = {
        "User-Agent": "MyGeocoderApp/1.0 (platon.kurbatov87@gmail.com)"
    }
    params = {"q": address, "format": "json", "limit": 1, "accept-language": "ru"}

    full_address = await return_address_if_exist(address)
    if full_address is None:
        try:
            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params=params,
                headers=headers,
                timeout=10,
            )
            if response.ok:
                data = response.json()
                if data:
                    await parse.parse_output_address(address, data[0])
                else:
                    print("Адрес не найден")
            else:
                print(f"Ошибка HTTP: {response.status_code}")
        except Exception as e:
            print(f"Ошибка запроса: {e}")
    else:
        print(f"Широта: {full_address.latitude}")
        print(f"Долгота: {full_address.longitude}")
        print(f"Полный адрес: {full_address.full_address}")