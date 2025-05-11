import parsing as parse

def show_help():
    print("""
Доступные команды:
1 — Ввести координаты (широта и долгота)
2 — Ввести адрес (город, улица, дом)
--help — Показать справку
exit — Выйти из программы
""")

def main():
    print("Добро пожаловать в гео-парсер!")

    while True:
        print("\nВведите команду (или --help):")
        command = input().strip().lower()

        if command == "exit":
            print("Выход из программы.")
            break
        elif command in ("--help", "-h"):
            show_help()
        elif command in ("1", "2"):
            parse.choose_input(command)
        else:
            print("Неизвестная команда. Введите --help для справки.")

if __name__ == '__main__':
    main()