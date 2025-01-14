import os
import sys
import importlib
import datetime
import json

keys_db = [
    {"key": "MAGISKY-DB-TOOL", "expiry_date": "2052-12-31", "tags": ["creator", "beta"]},
    {"key": "3TO0o3i7gVBGq1iM1dZJ", "expiry_date": "2025-01-15", "tags": ["user", "school", "secured"]},
    {"key": "guest", "expiry_date": "2025-01-15", "tags": ["guest", "school"]},
]

key_info = None
key_validated = False  # Флаг для проверки вывода сообщения

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_key():
    global key_info
    key_name = "key.txt"

    if os.path.exists(key_name):
        with open(key_name, "r", encoding="utf-8") as file:
            user_key = file.read().strip()
            if validate_key(user_key):
                return key_info

    user_key = input("Введите ключ: ").strip()
    if validate_key(user_key):
        with open(key_name, "w", encoding="utf-8") as file:
            file.write(user_key)
        return key_info

    print("Ключ не найден.")
    sys.exit()

def validate_key(user_key):
    global key_validated
    for record in keys_db:
        if record["key"] == user_key:
            expiry_date_str = record.get("expiry_date", "")
            if expiry_date_str:
                expiry_date = datetime.datetime.strptime(expiry_date_str, "%Y-%m-%d")
                if expiry_date >= datetime.datetime.now():
                    if not key_validated:
                        print("Ключ действителен.")
                        key_validated = True
                    global key_info
                    key_info = record
                    return True
                else:
                    print("Ключ просрочен.")
                    sys.exit()
            else:
                print("Дата истечения срока действия ключа отсутствует.")
                sys.exit()
    return False

def get_API():
    global API_ID, API_HASH, file_name
    file_name = "api_credentials.txt"
    if os.path.exists(file_name):
        try:
            with open(file_name, "r") as file:
                lines = file.readlines()
                API_ID = lines[0].split(":")[1].strip()
                API_HASH = lines[1].split(":")[1].strip()
                print(f"API_ID: {API_ID}")
                print(f"API_HASH: {API_HASH}")
                return API_ID, API_HASH
        except FileNotFoundError:
            print(f"Файл '{file_name}' не найден. Убедитесь, что он существует.")
            return None, None
        except IndexError:
            print(f"Файл '{file_name}' имеет неверный формат. Проверьте его содержимое.")
            return None, None
    else:
        API_ID = int(input("Введите API_ID: "))
        API_HASH = input("Введите API_HASH: ")
        with open(file_name, "w") as file:
            file.write(f"API_ID: {API_ID}\n")
            file.write(f"API_HASH: {API_HASH}\n")

def restart_program():
    clear_console()