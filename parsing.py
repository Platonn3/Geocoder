import response as req
def get_address():
    print("Введите город:")
    city = input()
    print("Введите улицу:")
    street = input()
    print("Введите номер дома:")
    number = input()
    address = f"{street} {number} {city}"
    req.get_full_address(address)
