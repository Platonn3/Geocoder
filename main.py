import sys
import asyncio
from Source import parsing as parse
from Source.database.models import init_db


def show_help():
    """Выводит справку по доступным командам"""
    print("""
Доступные команды:
1 — Ввести координаты (широта и долгота)
2 — Ввести адрес (город, улица, дом)
--help — Показать справку
exit — Выйти из программы

Примеры использования:
python main.py --help  # Показать справку
python main.py exit    # Выйти из программы
""")


async def process_command(command: str):
    if command == "exit":
        print("Выход из программы.")
        sys.exit(0)
    elif command in ("--help", "-h"):
        show_help()
    elif command in ("1", "2"):
        await parse.choose_input(command)
    else:
        print("Неизвестная команда. Введите --help для справки.")


async def interactive_mode():
    print("Добро пожаловать в Geocoder (интерактивный режим)!")
    try:
        while True:
            print("\nВведите команду (или --help):")
            command = input().strip().lower()
            await process_command(command)
    except (EOFError, StopIteration):
        print("Завершение из-за окончания ввода.")
        sys.exit(0)


async def main():
    await init_db()

    if len(sys.argv) > 1:
        command = sys.argv[1].strip().lower()
        if command in ("--help", "-h"):
            show_help()
            sys.exit(0)
        elif command == "exit":
            print("Выход из программы.")
            sys.exit(0)
        elif command in ("1", "2"):
            await parse.choose_input(command)
            sys.exit(0)
        else:
            print(f"Неизвестная команда: {command}")
            show_help()
            sys.exit(1)

    await interactive_mode()


if __name__ == '__main__':
    asyncio.run(main())