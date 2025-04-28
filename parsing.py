import response as req
def get_address():
    print("Введите адреc:")
    address = input()
    req.get_full_address(address)
