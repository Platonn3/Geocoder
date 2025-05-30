import asyncio
from Source import response as req
from Source.database.requests import add_new_address
from dadata import Dadata
from typing import Optional, Dict

token = "a2c67eb60ada13b05220830b7ea4611ae28e7ab9"
secret = "8236c69efae9d50b7c4b2c064ec863901424d4a5"
dadata = Dadata(token, secret)


def clean_address(address: str) -> Optional[Dict]:
    try:
        return dadata.clean("address", address)
    except Exception as e:
        print(f"[Ошибка Dadata] Не удалось очистить адрес: {e}")
        return None


def build_normalized_address(cleaned_data: Dict) -> Optional[str]:
    try:
        fields_order = ['street', 'house', 'city', 'region', 'country']
        parts = [cleaned_data[field] for field in fields_order if cleaned_data.get(field)]

        if not parts:
            print("Не удалось построить нормализованный адрес — все поля пусты")
            return None

        return ' '.join(parts)
    except (KeyError, TypeError) as e:
        print(f"[Ошибка сборки адреса] Неверная структура данных: {e}")
        return None


async def parse_input_address():
    try:
        city = sanitize_input(input("Введите город: "))
        street = sanitize_input(input("Введите улицу: "))
        number = sanitize_input(input("Введите номер дома: "))
        address = f"{street} {number} {city} Россия"

        cleaned = clean_address(address)
        if not cleaned:
            print("Нормализация адреса не удалась")
            return

        normalized_address = build_normalized_address(cleaned)
        if not normalized_address:
            print("Не удалось собрать адрес из полученных данных")
            return

        try:
            await req.send_request(normalized_address)
        except Exception as e:
            print(f"[Ошибка отправки] Не удалось отправить адрес: {e}")

    except Exception as e:
        print(f"[Ошибка ввода] {e}")


async def parse_input_coordinates():
    try:
        coords = input("Введите широту и долготу через пробел: ").strip().split()
        if len(coords) != 2:
            raise ValueError("Нужно ввести две координаты")

        lat, lon = float(coords[0]), float(coords[1])

        try:
            await req.send_request(f"{lat} {lon}")
        except Exception as e:
            print(f"[Ошибка отправки координат] {e}")

    except ValueError:
        print("Координаты должны быть числами (пример: 55.7558 37.6173)")
    except Exception as e:
        print(f"[Ошибка координат] {e}")


async def parse_output_address(input_address: str, output_address: Dict):
    try:
        if not output_address:
            print("Пустой ответ от геокодера")
            return

        full_address = output_address.get("display_name")
        lat = output_address.get("lat")
        lon = output_address.get("lon")

        if not all([full_address, lat, lon]):
            print("Отсутствуют необходимые данные в ответе")
            return

        if not full_address.endswith("Россия"):
            print("Адрес не находится в России")
            return

        await add_new_address(input_address, full_address, lat, lon)
        print(f"Адрес сохранён\nШирота: {lat}\nДолгота: {lon}\nПолный адрес: {full_address}")

    except Exception as e:
        print(f"[Ошибка обработки ответа] {e}")


def sanitize_input(text: str) -> str:
    return text.encode('utf-8', errors='ignore').decode('utf-8').strip()


async def choose_input(choice: str):
    try:
        if choice == "1":
            await parse_input_coordinates()
        elif choice == "2":
            await parse_input_address()
        else:
            print("Введите 1 (координаты) или 2 (адрес)")
    except Exception as e:
        print(f"[Ошибка выбора] {e}")
