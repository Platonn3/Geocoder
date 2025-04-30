import response as req

def parse_input_address():
    print("Введите город:")
    city = input()
    print("Введите улицу:")
    street = input()
    print("Введите номер дома:")
    number = input()
    address = f"{street} {number} {city}"
    req.get_full_address(address)

def parse_output_address(address):
    print(f"Широта : {address["lat"]}")
    print(f"Долгота : {address["lon"]}")
    full_address = address["display_name"]
    parts = full_address.split(",")
    result_address = str()
    for i in range(len(parts) - 1, -1, -1):
        result_address += f"{parts[i].strip()}"
        if i != 0:
            result_address += ", "
    print(result_address)
