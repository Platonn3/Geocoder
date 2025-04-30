import response as req


def choose_input():
    print("Нажмите 1, если хотите ввести широту и долготу")
    print("Нажмите 2, если хотите ввести адрес")
    number = input()
    try:
        if int(number) == 1:
            parse_input_coordinates()
        elif int(number) == 2:
            parse_input_address()
        else:
            print("Ошибка ввода, выберете 1 или 2 вариант")
    except ValueError:
        print("Ошибка ввода, выберете 1 или 2 вариант")

def parse_input_address():
    print("Введите город:")
    city = input()
    print("Введите улицу:")
    street = input()
    print("Введите номер дома:")
    number = input()
    address = f"{street} {number} {city} Россия"
    req.get_full_address(address)

def parse_input_coordinates():
    print("Введите широту")
    lat = input()
    print("Введите долготу")
    lon = input()
    address = f"{lat} {lon}"
    req.get_full_address(address)

def parse_output_address(address):
    print(f"Широта : {address["lat"]}")
    print(f"Долгота : {address["lon"]}")
    full_address = address["display_name"]
    parts = full_address.split(", ")
    result_address = str()
    for i in range(len(parts) - 1, -1, -1):
        result_address += f"{parts[i].strip()}"
        if i != 0:
            result_address += ", "
    print(result_address)
