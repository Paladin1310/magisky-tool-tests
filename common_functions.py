import asyncio
import importlib
import shutil
import socket
import subprocess
import sys
import os
import datetime
import logging
import threading
import platform
import paramiko
import telethon
import tqdm
import json
import re
import psutil
from telethon.sync import TelegramClient, events

from utils import check_key, get_API, restart_program
def lud():
    async def execute_command(command):
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if stderr:
                print(f"Ошибка: {stderr.decode('cp866').strip()}")
            return stdout.decode('cp866').strip()
        except Exception as e:
            print(f"Ошибка выполнения команды: {e}")
            return None

    def parse_users(output):
        users = []
        for line in output.splitlines():
            line = line.strip()
            if (
                    line
                    and not line.startswith("Учетные записи пользователей для")
                    and not line.startswith("Команда выполнена успешно")
                    and not line.startswith("-----")
            ):
                users.extend(line.split())
        return users

    async def process_user(user, local_info_list):
        user_command = f"net user \"{user}\""
        user_info = await execute_command(user_command)
        if user_info:
            user_file = os.path.join(local_info_list, f"{user}.txt")
            with open(user_file, "w", encoding="utf-8") as f:
                f.write(user_info)
            print(f"Информация о пользователе {user} сохранена в {user_file}.")
        else:
            print(f"Не удалось получить информацию о пользователе {user}.")

    async def local_user_dump():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        local_users_list = os.path.join(base_dir, "local_users_list")
        local_info_list = os.path.join(base_dir, "local_info_list")

        os.makedirs(local_users_list, exist_ok=True)
        os.makedirs(local_info_list, exist_ok=True)

        command = "net user"
        output = await execute_command(command)
        if not output:
            print("Не удалось получить список пользователей.")
            return

        domain_users_file = os.path.join(local_users_list, "users.txt")
        with open(domain_users_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Список пользователей сохранен в {domain_users_file}.")

        users = parse_users(output)
        if not users:
            print("Не удалось распознать пользователей. Проверьте вывод команды.")
            return

        semaphore = asyncio.Semaphore(10)
        tasks = []

        async def limited_process_user(user):
            async with semaphore:
                await process_user(user, local_info_list)

        for user in users:
            tasks.append(limited_process_user(user))

        await asyncio.gather(*tasks)

    asyncio.run(local_user_dump())

def dud():
    async def execute_command(command):
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if stderr:
                error_message = stderr.decode('cp866').strip()
                print(f"Ошибка: {error_message}")
                return None, error_message
            return stdout.decode('cp866').strip(), None
        except Exception as e:
            print(f"Ошибка выполнения команды: {e}")
            return None, str(e)

    def parse_users(output):
        users = []
        for line in output.splitlines():
            line = line.strip()
            if (
                    line
                    and not line.startswith("Учетные записи пользователей для")
                    and not line.startswith("Команда выполнена успешно")
                    and not line.startswith("-----")
            ):
                users.extend(line.split())
        return users

    async def process_user(user, db_info_users_domain):
        user_command = f"net user \"{user}\" /domain"
        user_info, error = await execute_command(user_command)
        if user_info:
            user_file = os.path.join(db_info_users_domain, f"{user}.txt")
            with open(user_file, "w", encoding="utf-8") as f:
                f.write(user_info)
            print(f"Информация о пользователе {user} сохранена в {user_file}.")
        else:
            print(f"Не удалось получить информацию о пользователе {user}. Ошибка: {error}")

    async def domain_user_dump():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        list_user_domain = os.path.join(base_dir, "list_user_domain")
        db_info_users_domain = os.path.join(base_dir, "db_info_users_domain")

        os.makedirs(list_user_domain, exist_ok=True)
        os.makedirs(db_info_users_domain, exist_ok=True)

        command = "net user /domain"
        output, error = await execute_command(command)
        if not output:
            print(f"Не удалось получить список пользователей. Ошибка: {error}")
            return

        domain_users_file = os.path.join(list_user_domain, "domain_users.txt")
        with open(domain_users_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Список пользователей сохранен в {domain_users_file}.")

        users = parse_users(output)
        if not users:
            print("Не удалось распознать пользователей. Проверьте вывод команды.")
            return

        semaphore = asyncio.Semaphore(10)
        tasks = []

        async def limited_process_user(user):
            async with semaphore:
                await process_user(user, db_info_users_domain)

        for user in users:
            tasks.append(limited_process_user(user))

        await asyncio.gather(*tasks)

    asyncio.run(domain_user_dump())



def st():
    def execute_command(command, shell_type):
        """
        Выполняет указанную команду в выбранной оболочке (PowerShell или CMD для Windows, shell для Linux и macOS).
        """
        if platform.system() == "Windows":
            if shell_type == "powershell":
                shell = shutil.which("powershell")
            else:
                shell = shutil.which("cmd.exe")
        else:
            shell = "/bin/bash"

        process = subprocess.Popen(command, shell=True, text=True, executable=shell,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='cp866')

        for line in process.stdout:
            print(line, end='')

        for line in process.stderr:
            print(line, end='')

    def main():
        if platform.system() == "Windows":
            shell_type = input("Выберите оболочку для выполнения команды (powershell/cmd): ").strip().lower()
            if shell_type not in ["powershell", "cmd"]:
                print("Ошибка: неверный выбор оболочки!")
                return
        else:
            shell_type = "bash"

        command = input("Введите команду для выполнения: ").strip()

        try:
            repetitions = int(input("Сколько раз выполнить команду? "))
            if repetitions <= 0:
                print("Ошибка: количество повторений должно быть положительным!")
                return
        except ValueError:
            print("Ошибка: необходимо ввести целое число!")
            return

        use_threads = input("Использовать потоки? (да/нет): ").strip().lower()
        if use_threads == "да":
            try:
                thread_count = int(input("Сколько потоков использовать? "))
                if thread_count <= 0:
                    print("Ошибка: количество потоков должно быть положительным!")
                    return
            except ValueError:
                print("Ошибка: необходимо ввести целое число!")
                return

            threads = []
            for _ in range(repetitions):
                thread = threading.Thread(target=execute_command, args=(command, shell_type))
                threads.append(thread)
                thread.start()

                if len(threads) >= thread_count:
                    for t in threads:
                        t.join()
                    threads = []

            for t in threads:
                t.join()

        else:
            for _ in range(repetitions):
                execute_command(command, shell_type)

    print("Начало стресс-теста...")
    main()

# -------------------------------------------------------------------------------------
# Настройки
# -------------------------------------------------------------------------------------

ACCOUNTS_FILE = 'accounts.json'     # Хранилище аккаунтов (phone + session_name)
ALGORITHMS_FILE = 'algorithms.json' # Хранилище алгоритмов

# -------------------------------------------------------------------------------------
# Утилиты для JSON-хранилища
# -------------------------------------------------------------------------------------
def load_json(path: str) -> list:
    """Загрузить список (или вернуть пустой список, если файла нет)."""
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path: str, data: list) -> None:
    """Сохранить список data в JSON-файл."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# -------------------------------------------------------------------------------------
# Менеджер аккаунтов (async)
# -------------------------------------------------------------------------------------
async def add_new_account() -> dict:
    """
    Добавить новый аккаунт (асинхронно):
      - запросить телефон
      - отправить код в Telegram
      - авторизация (2FA, если нужно)
      - сохранить в accounts.json
    """

    phone = input("Введите номер телефона (формат +79998887766): ").strip()
    if not phone:
        print("Ошибка: номер телефона не может быть пустым.")
        return {}
    session_name = f"session_{phone.replace('+','').replace('-','')}"

    tmp_client = TelegramClient(
        session_name,
        API_ID,
        API_HASH,
        device_model="iPhone 14 Pro",
        system_version="iOS 17.1"
    )

    await tmp_client.connect()

    if not await tmp_client.is_user_authorized():
        print(f"Отправляем код на {phone}...")
        await tmp_client.send_code_request(phone)
        code = input("Введите код из Telegram/SMS: ").strip()
        try:
            await tmp_client.sign_in(phone, code)
        except telethon.errors.SessionPasswordNeededError:
            password = input("У вас настроен облачный пароль (2FA). Введите его: ")
            await tmp_client.sign_in(password=password)
        except Exception as e:
            raise e
    else:
        print("Уже авторизованы.")

    await tmp_client.disconnect()

    accounts = load_json(ACCOUNTS_FILE)
    new_acc = {"phone": phone, "session_name": session_name}
    accounts.append(new_acc)
    save_json(ACCOUNTS_FILE, accounts)
    print(f"Аккаунт [{phone}] добавлен и сохранён.")
    return new_acc

async def choose_account() -> dict:
    """
    Показать список аккаунтов, дать выбрать или добавить новый.
    Возвращает { 'phone':..., 'session_name':... }.
    """
    accounts = load_json(ACCOUNTS_FILE)
    if not accounts:
        print("Список аккаунтов пуст, нужно добавить новый.")
        return await add_new_account()

    print("\nСуществующие аккаунты:")
    for idx, acc in enumerate(accounts, start=1):
        print(f"[{idx}] {acc['phone']}")
    print("[0] Добавить новый аккаунт")

    while True:
        choice = input("Выберите номер аккаунта или 0: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if choice == 0:
                return await add_new_account()
            elif 1 <= choice <= len(accounts):
                return accounts[choice - 1]
        print("Некорректный ввод. Повторите.")

# -------------------------------------------------------------------------------------
# Менеджер алгоритмов
# -------------------------------------------------------------------------------------
def list_algorithms_menu():
    """
    Главное меню менеджера алгоритмов:
      0  - Запустить все алгоритмы (выбор аккаунта, запуск)
      -1 - Выход
      -2 - Создать новый
      [N] - Редактировать алгоритм с индексом N
    """
    while True:
        algorithms = load_json(ALGORITHMS_FILE)
        if not algorithms:
            print("\nСписок алгоритмов пуст.")
        else:
            print("\nСписок алгоритмов:")
            for idx, algo in enumerate(algorithms, start=1):
                print(f"[{idx}] trigger_text='{algo['trigger_text']}', steps={len(algo['steps'])}, loop_count={algo['loop_count']}")

        print("[0] Запустить все алгоритмы")
        print("[-1] Выход")
        print("[-2] Создать новый алгоритм")

        choice = input("Выберите действие: ").strip()
        if choice == '0':
            # Запустить все алгоритмы
            print("Запуск всех алгоритмов...")
            asyncio.run(run_all_algorithms())
        elif choice == '-1':
            print("Выход из менеджера алгоритмов.")
            return
        elif choice == '-2':
            # Создать новый
            new_algo = create_algorithm()
            if new_algo:
                algorithms.append(new_algo)
                save_json(ALGORITHMS_FILE, algorithms)
                print("Новый алгоритм добавлен.")
        else:
            # Попытка выбрать алгоритм для редактирования
            if choice.isdigit():
                choice_idx = int(choice)
                if 1 <= choice_idx <= len(algorithms):
                    edited = edit_algorithm(choice_idx - 1)
                    if edited == "deleted":
                        pass  # Алгоритм удалён, возвращаемся к списку
            else:
                print("Некорректный ввод.")


def create_algorithm() -> dict:
    """
    Создаём новый алгоритм:
      - trigger_text
      - loop_count
      - steps (список {action='edit', text='...', delay=N})
    """
    print("\n=== Создание нового алгоритма ===")
    trigger_text = input("Введите trigger_text (сообщение-триггер): ").strip()
    if not trigger_text:
        print("Триггер не может быть пустым. Отмена создания.")
        return {}

    loop_str = input("Сколько раз повторять (0 = бесконечно)? ").strip()
    try:
        loop_count = int(loop_str)
    except:
        loop_count = 1

    steps = []
    print("Добавляем шаги: для каждого шага введите:")
    print(" - Текст, на который редактируем")
    print(" - Задержка (сек) после шага")
    print("Оставьте текст пустым, чтобы закончить ввод шагов.")

    while True:
        txt = input("Текст (пусто = конец): ").strip()
        if not txt:
            break
        delay_str = input("Задержка (сек)? ").strip()
        try:
            delay = int(delay_str)
        except:
            delay = 0
        step = {"action": "edit", "text": txt, "delay": delay}
        steps.append(step)

    algo = {
        "trigger_text": trigger_text,
        "loop_count": loop_count,
        "steps": steps
    }
    return algo


def edit_algorithm(index: int) -> str:
    """
    Редактирование существующего алгоритма (по индексу в списке).
    Показываем строки:
      1) trigger_text
      2) loop_count
      3...) шаги
    Меню:
      [0] - выход из редактирования
      [-1] - удалить весь алгоритм
      [N] - отредактировать строку N
    Возвращает:
      ""        - если отредактирован
      "deleted" - если алгоритм удалён
    """
    algorithms = load_json(ALGORITHMS_FILE)
    if not (0 <= index < len(algorithms)):
        return ""

    algo = algorithms[index]

    while True:
        print("\n=== Редактирование алгоритма ===")
        print("1) trigger_text =", algo['trigger_text'])
        print("2) loop_count   =", algo['loop_count'])
        steps = algo.get('steps', [])
        if not steps:
            print("Нет шагов.")
        else:
            for i, step in enumerate(steps, start=3):
                print(f"{i}) step: action={step['action']}, text='{step['text']}', delay={step['delay']}")

        print("\n[0] - выход из редактирования")
        print("[-1] - удалить весь алгоритм")

        choice = input("Введите номер строки для редактирования: ").strip()
        if choice == '0':
            save_json(ALGORITHMS_FILE, algorithms)
            return ""
        elif choice == '-1':
            confirm = input("Точно удалить алгоритм? (yes/no): ").strip().lower()
            if confirm == 'yes':
                algorithms.pop(index)
                save_json(ALGORITHMS_FILE, algorithms)
                print("Алгоритм удалён.")
                return "deleted"
            else:
                print("Отмена удаления.")
        else:
            if choice.isdigit():
                cnum = int(choice)
                if cnum == 1:
                    # Редактируем trigger_text
                    new_val = input("Новое значение trigger_text: ").strip()
                    if new_val:
                        algo['trigger_text'] = new_val
                        print("trigger_text обновлён.")
                elif cnum == 2:
                    new_val = input("Новое значение loop_count: ").strip()
                    try:
                        new_val_int = int(new_val)
                        algo['loop_count'] = new_val_int
                        print("loop_count обновлён.")
                    except:
                        print("Некорректное число, отмена.")
                else:
                    # Редактируем шаг (3 -> steps[0], 4 -> steps[1], ...)
                    step_index = cnum - 3
                    if 0 <= step_index < len(steps):
                        print(f"Старый шаг: text='{steps[step_index]['text']}', delay={steps[step_index]['delay']}")
                        new_text = input("Новый текст (Enter, чтобы оставить тот же): ")
                        if new_text:
                            steps[step_index]['text'] = new_text

                        new_delay = input("Новый delay (сек, Enter=пропустить): ").strip()
                        if new_delay:
                            if new_delay.isdigit():
                                steps[step_index]['delay'] = int(new_delay)
                            else:
                                print("Некорректный delay, пропускаем.")
                        print("Шаг обновлён.")
                    else:
                        print("Нет такого шага.")
                save_json(ALGORITHMS_FILE, algorithms)
            else:
                print("Некорректный ввод.")


# -------------------------------------------------------------------------------------
# Запуск всех алгоритмов + Telethon + команды /timer, /secund
# -------------------------------------------------------------------------------------

# Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def run_all_algorithms():
    """
    Спросить, с какого аккаунта запускать.
    Затем запустить Telethon, слушать исходящие сообщения.
    Для КАЖДОГО алгоритма, если event.raw_text == trigger_text, выполняем steps.
    Добавлены команды /timer <sec> и /secund (простой пример «секундомера»).
    """
    account = await choose_account()
    if not account:
        return

    algorithms = load_json(ALGORITHMS_FILE)
    session_name = account["session_name"]
    client = TelegramClient(session_name, API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        logging.error("Аккаунт не авторизован. Завершаем.")
        await client.disconnect()
        return

    logging.info(f"Аккаунт {account['phone']} авторизован. Сессия: {session_name}")

    @client.on(events.NewMessage(outgoing=True))
    async def handler(event):
        text = event.raw_text.strip()
        logging.info(f"Новое исходящее сообщение: {text}")

        # --- 1. Обработка КОМАНД (не из алгоритмов) ---
        # /timer <N>
        if text.startswith("/timer "):
            parts = text.split()
            if len(parts) == 2 and parts[1].isdigit():
                sec = int(parts[1])
                # Отвечаем сообщением (reply)
                reply_msg = await event.reply(f"Таймер до {sec} секунд запущен.")
                logging.info(f"Таймер до {sec} секунд запущен.")
                # Запускаем отдельную "задачу", чтобы не блокировать обработчик
                async def timer_task():
                    await asyncio.sleep(sec)
                    await event.reply(f"Прошло {sec} секунд.")
                    logging.info(f"Прошло {sec} секунд.")
                asyncio.create_task(timer_task())
                return  # Команду обработали, не ищем совпадений в алгоритмах

        # /secund
        elif text == "/second":
            # Запускаем «секундомер» на 10 секунд (пример)
            msg = await event.reply("Секундомер запущен. Прошло 0 секунд.")
            logging.info("Секундомер запущен.")
            async def secund_task():
                for i in range(1, 9999):
                    await asyncio.sleep(1)
                    try:
                        await msg.edit(f"Секундомер запущен. Прошло {i} секунд.")
                        logging.info(f"Секундомер: {i} секунд.")
                    except:
                        pass
                # Можно доп. сообщение «Остановлен» или просто оставить как есть
                await msg.reply("Секундомер завершён (9999 секунд).")
                logging.info("Секундомер завершён (9999 секунд).")
            asyncio.create_task(secund_task())
            return

        # --- 2. Проверяем алгоритмы (trigger_text) ---
        for algo in algorithms:
            if text == algo.get("trigger_text"):
                steps = algo.get("steps", [])
                loop_count = algo.get("loop_count", 1)
                logging.info(f"Алгоритм найден: {algo['trigger_text']}, шагов: {len(steps)}, циклов: {loop_count}")
                # Выполняем цикл редактирований
                cycles = 0
                while True:
                    cycles += 1
                    for step in steps:
                        if step.get("action") == "edit":
                            new_text = step.get("text", "")
                            try:
                                await event.edit(new_text)
                                logging.info(f"Сообщение изменено на: {new_text}")
                            except:
                                pass
                            delay = step.get("delay", 0)
                            if delay > 0:
                                await asyncio.sleep(delay)
                                logging.info(f"Задержка: {delay} секунд.")
                    # Если loop_count=0 => бесконечно
                    if loop_count != 0 and cycles >= loop_count:
                        break
                break  # Если нашли алгоритм, не даём совпасть с другими

    print("\nВсе алгоритмы и команды (/timer, /second) запущены. Нажмите Enter для остановки...")
    logging.info("Все алгоритмы и команды запущены.")
    stop_event = threading.Event()

    def wait_enter():
        input()
        stop_event.set()

    t = threading.Thread(target=wait_enter, daemon=True)
    t.start()

    while not stop_event.is_set():
        await asyncio.sleep(0.3)

    print("Останавливаем клиент...")
    logging.info("Останавливаем клиент...")
    await client.disconnect()
    logging.info("Готово.")

# -------------------------------------------------------------------------------------
# Главное меню
# -------------------------------------------------------------------------------------
def main_menu():
    while True:
        print("\n=== Главное меню ===")
        print("[1] Менеджер аккаунтов")
        print("[2] Менеджер алгоритмов")
        print("[-1] Выход")

        choice = input("Выберите: ").strip()
        if choice == '1':
            asyncio.run(async_accounts_menu())
        elif choice == '2':
            list_algorithms_menu()
        elif choice == '-1':
            print("Выход.")
            restart_program()
            break
        else:
            print("Некорректный ввод.")

async def async_accounts_menu():
    """
    Простейшее меню для аккаунтов:
    - Показ списка
    - [0] Добавить новый
    - [-1] выход
    """
    while True:
        accounts = load_json(ACCOUNTS_FILE)
        if not accounts:
            print("\n(Нет аккаунтов)")
        else:
            print("\nСписок аккаунтов:")
            for i, acc in enumerate(accounts, start=1):
                print(f"[{i}] {acc['phone']} (session={acc['session_name']})")
        print("[0] Добавить новый аккаунт")
        print("[-1] Выход в главное меню")

        choice = input("Выберите: ").strip()
        if choice == '-1':
            return
        elif choice == '0':
            await add_new_account()
        else:
            if choice.isdigit():
                cidx = int(choice)
                if 1 <= cidx <= len(accounts):
                    print(f"Вы выбрали аккаунт {accounts[cidx-1]['phone']}. Пока действий нет, возвращаемся.")
            else:
                print("Некорректный ввод.")

def tgmain():
    main_menu()

keys_db = [
    {"key": "MAGISKY-DB-TOOL", "expiry_date": "2052-12-31", "tags": ["creator"]},
    {"key": "3TO0o3i7gVBGq1iM1dZJ", "expiry_date": "2025-01-10", "tags": ["user", "school", "secured"]},
]

def ssh():
    host = input("Введите SSH хост: ")
    port = int(input("Введите SSH порт (по умолчанию 22): ") or 22)
    username = input("Введите SSH имя пользователя: ")
    password = input("Введите SSH пароль: ")

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print("Подключение...")
        ssh_client.connect(hostname=host, port=port, username=username, password=password)
        print(f"Успешное подключение к {host}")

        while True:
            command = input(f"{username}@{host}:~$ ")
            if command.lower() in ["exit", "quit"]:
                print("Завершение сессии...")
                break

            stdin, stdout, stderr = ssh_client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            if output:
                print(output)
            if error:
                print("Ошибка:", error)

    except paramiko.ssh_exception.AuthenticationException:
        print("Ошибка аутентификации! Проверьте имя пользователя и пароль.")
    except paramiko.ssh_exception.SSHException as e:
        print("Ошибка SSH:", e)
    except Exception as e:
        print("Общая ошибка:", e)
    finally:
        ssh_client.close()
        print("Соединение закрыто.")

import concurrent.futures

def scan_port(target, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        result = s.connect_ex((target, port))
        if result == 0:
            return port
    except Exception:
        pass
    finally:
        s.close()
    return None

def simple_nmap():
    print("=== Скан портов ===")
    target = input("Введите IP-адрес или доменное имя для сканирования: ").strip()
    maxw = int(input("Введите количество потоков (по умолчанию 100): ") or 100)
    popular_ports = [
        1, 3, 7, 9, 13, 17, 19, 20, 21, 22, 23, 25, 26, 37, 53, 79, 80, 81, 82, 83, 84, 85,
        88, 89, 90, 99, 100, 106, 110, 111, 113, 119, 135, 139, 143, 144, 179, 199, 211, 212,
        222, 254, 255, 256, 259, 264, 280, 301, 306, 311, 340, 366, 389, 406, 407, 416, 417,
        425, 427, 443, 444, 445, 458, 464, 465, 481, 497, 500, 512, 513, 514, 515, 524, 541,
        543, 544, 545, 548, 554, 555, 563, 587, 593, 616, 617, 625, 631, 636, 646, 648, 666,
        667, 668, 683, 687, 691, 700, 705, 711, 714, 720, 722, 726, 749, 765, 777, 783, 787,
        800, 801, 808, 843, 873, 880, 888, 898, 900, 901, 902, 903, 911, 912, 981, 987, 990,
        992, 993, 995, 999, 1000, 1001, 1002, 1007, 1009, 1010, 1011, 1021, 1022, 1023, 1024,
        1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038,
        1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052,
        1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066,
        1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080,
        1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094,
        1095, 1096, 1097, 1098, 1099, 1100, 1102, 1104, 1105, 1106, 1107, 1108, 1110, 1111,
        1112, 1113, 1114, 1117, 1119, 1121, 1122, 1123, 1124, 1126, 1130, 1131, 1132, 1137,
        1138, 1141, 1145, 1147, 1148, 1149, 1151, 1152, 1154, 1163, 1164, 1165, 1166, 1169,
        1174, 1175, 1183, 1185, 1186, 1187, 1192, 1198, 1199, 1201, 1213, 1216, 1217, 1218,
        1233, 1234, 1236, 1244, 1247, 1248, 1259, 1271, 1272, 1277, 1287, 1296, 1300, 1301,
        1309, 1310, 1311, 1322, 1328, 1334, 1352, 1417, 1433, 1434, 1443, 1455, 1461, 1494,
        1500, 1501, 1503, 1521, 1524, 1533, 1556, 1580, 1583, 1594, 1600, 1641, 1658, 1666,
        1687, 1688, 1700, 1716, 1717, 1721, 1723, 1755, 1761, 1782, 1801, 1805, 1812, 1839,
        1840, 1862, 1863, 1864, 1875, 1900, 1914, 1935, 1947, 1971, 1972, 1974, 1984, 1998,
        1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2013, 2020,
        2021, 2022, 2030, 2033, 2034, 2035, 2038, 2040, 2041, 2042, 2043, 2045, 2046, 2047,
        2048, 2049, 2065, 2068, 2099, 2100, 2103, 2105, 2106, 2107, 2111, 2119, 2121, 2126,
        2135, 2144, 2160, 2161, 2170, 2179, 2190, 2191, 2196, 2200, 2222
    ]

    popular_ports_set = set(popular_ports)
    open_ports = []

    print(f"\nСканируем популярные порты ({len(popular_ports)}) на хосте {target}...\n")

    start_time_popular = datetime.datetime.now()

    with concurrent.futures.ThreadPoolExecutor(max_workers=maxw) as executor:
        future_to_port = {executor.submit(scan_port, target, port): port for port in popular_ports}
        for future in tqdm.tqdm(concurrent.futures.as_completed(future_to_port), total=len(popular_ports), desc="Скан популярных портов"):
            port = future_to_port[future]
            if future.result():
                open_ports.append(port)
                print(f"[Популярный] Порт {port} открыт")

    end_time_popular = datetime.datetime.now()
    popular_scan_time = end_time_popular - start_time_popular
    print(f"\nСканирование популярных портов завершено за: {popular_scan_time}")

    print(f"\nНачинаем полное сканирование остальных портов на хосте {target}...\n"
          "Это может занять ОЧЕНЬ много времени...\n")

    start_time_rest = datetime.datetime.now()

    with concurrent.futures.ThreadPoolExecutor(max_workers=maxw) as executor:
        future_to_port = {executor.submit(scan_port, target, port): port for port in range(1, 65536) if port not in popular_ports_set}
        for future in tqdm.tqdm(concurrent.futures.as_completed(future_to_port), total=65535 - len(popular_ports), desc="Скан остальных портов"):
            port = future_to_port[future]
            if future.result():
                open_ports.append(port)
                print(f"[Остальные] Порт {port} открыт")
            if port % 100 == 0:
                print(f"Проверяется порт: {port}")

    end_time_rest = datetime.datetime.now()
    rest_scan_time = end_time_rest - start_time_rest
    print(f"\nСканирование всех остальных портов завершено за: {rest_scan_time}")

    total_time = (end_time_rest - start_time_popular)
    print(f"Полное время сканирования (популярные + остальные): {total_time}")

    print("\nВсе открытые порты:")
    for port in open_ports:
        print(f"Порт {port} открыт")


def scan_system():
    print("Информация о системе:")
    print(f"Система: {platform.system()}")
    print(f"Имя узла: {platform.node()}")
    print(f"Релиз: {platform.release()}")
    print(f"Версия: {platform.version()}")
    print(f"Машина: {platform.machine()}")
    print(f"Процессор: {platform.processor()}")
    print(f"Архитектура: {platform.architecture()}")
    print(f"IP-адрес: {socket.gethostbyname(socket.gethostname())}")

    print("\nИнформация о процессоре:")
    print(f"Количество ядер: {psutil.cpu_count(logical=False)}")
    print(f"Количество логических процессоров: {psutil.cpu_count(logical=True)}")
    print(f"Частота процессора: {psutil.cpu_freq().current} MHz")

    print("\nИнформация о памяти:")
    virtual_memory = psutil.virtual_memory()
    print(f"Всего памяти: {virtual_memory.total / (1024 ** 3):.2f} GB")
    print(f"Доступно памяти: {virtual_memory.available / (1024 ** 3):.2f} GB")
    print(f"Использовано памяти: {virtual_memory.used / (1024 ** 3):.2f} GB")
    print(f"Процент использования памяти: {virtual_memory.percent}%")

    print("\nИнформация о дисках:")
    for partition in psutil.disk_partitions():
        print(f"Диск: {partition.device}")
        print(f"  Точка монтирования: {partition.mountpoint}")
        print(f"  Файловая система: {partition.fstype}")
        usage = psutil.disk_usage(partition.mountpoint)
        print(f"  Всего: {usage.total / (1024 ** 3):.2f} GB")
        print(f"  Использовано: {usage.used / (1024 ** 3):.2f} GB")
        print(f"  Доступно: {usage.free / (1024 ** 3):.2f} GB")
        print(f"  Процент использования: {usage.percent}%")

    print("\nИнформация о сети:")
    for interface, addrs in psutil.net_if_addrs().items():
        print(f"Интерфейс: {interface}")
        for addr in addrs:
            if addr.family == socket.AF_INET:
                print(f"  IP-адрес: {addr.address}")
            elif platform.system() != "Windows" and addr.family == socket.AF_PACKET:
                print(f"  MAC-адрес: {addr.address}")


import nmap
import socket

import nmap
import socket

def scan_vulnerabilities():
    target = input("Введите IP-адрес или домен для сканирования: ")
    try:
        # Проверка разрешения доменного имени
        ip_address = socket.gethostbyname(target)
        print(f"IP-адрес для {target}: {ip_address}")
    except socket.gaierror:
        print("Не удалось разрешить доменное имя. Проверьте IP-адрес или домен.")
        return

    nm = nmap.PortScanner()
    print(f"Сканирование {target} ({ip_address}) на наличие уязвимостей...")
    try:
        nm.scan(ip_address, arguments='--unprivileged -sV --script=vuln')
        if not nm.all_hosts():
            print("Не удалось найти хост. Проверьте IP-адрес или домен.")
            return

        for host in nm.all_hosts():
            print(f"\nРезультаты сканирования для {host}:")
            found_vulnerabilities = False
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    print(f"Порт: {port}\tСостояние: {nm[host][proto][port]['state']}")
                    if 'script' in nm[host][proto][port]:
                        found_vulnerabilities = True
                        for script in nm[host][proto][port]['script']:
                            print(f"Уязвимость: {script}\nОписание: {nm[host][proto][port]['script'][script]}")
            if not found_vulnerabilities:
                print("Уязвимости не найдены.")
    except Exception as e:
        print(f"Ошибка при сканировании: {e}")


