import response as req


def choose_input():
    try:
        print("Нажмите 1, если хотите ввести широту и долготу")
        print("Нажмите 2, если хотите ввести адрес в виде: город, улица, номер дома")
        number = input()
        if int(number) == 1:
            parse_input_coordinates()
        elif int(number) == 2:
            parse_input_address()
        else:
            print("Ошибка ввода, выберете 1 или 2 вариант")
    except ValueError:
        print("Ошибка ввода, выберете 1 или 2 вариант")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


def parse_input_address():
    try:
        print("Введите город:")
        city = input()
        print("Введите улицу:")
        street = input()
        print("Введите номер дома:")
        number = input()
        address = f"{street} {number} {city} Россия"
        req.send_request(address)
    except Exception as e:
        print(f"Ошибка при вводе адреса: {e}")


def parse_input_coordinates():
    print("Введите широту и долготу")
    try:
        lat = float(input())
        lon = float(input())
        address = f"{lat} {lon}"
        req.send_request(address)
    except ValueError:
        print("Ошибка ввода координат. Убедитесь, что вводите числа.")
    except Exception as e:
        print(f"Ошибка при обработке координат: {e}")


def parse_output_address(address):
    try:
        full_address = address.get("display_name", "")
        lat = address.get("lat", "неизвестно")
        lon = address.get("lon", "неизвестно")

        if not full_address:
            print("Не удалось распознать адрес.")
            return

        parts = full_address.split(", ")
        if not parts or parts[-1] != "Россия":
            print("Введённый адрес находится не в России. Введите другой.")
            return

        print(f"Широта: {lat}")
        print(f"Долгота: {lon}")
        print("Полный адрес:", full_address)

    except Exception as e:
        print(f"Ошибка при обработке ответа: {e}")
