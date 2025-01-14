# function_definitions.py

import asyncio
import os
import platform
import beta
from utils import get_API
from common_functions import restart_program, scan_vulnerabilities, st, simple_nmap, tgmain, ssh, lud, dud, scan_system

def settings():
    print("Пока тут пусто")
    int(input("Нажмите enter для продолжения..."))
    return

def local_user_dump():
    if platform.system() != "Windows":
        print("Эта функция доступна только на Windows.")
        input("Нажмите enter для продолжения...")
        return

    num = int(input("Вы уверены? (local user dump) 0/1?:"))
    if num == 1:
        print("Запуск...")
        lud()
        input("Нажмите enter для продолжения...")
    else:
        print("OK")

def domain_user_dump(domain_user_block):
    if platform.system() != "Windows":
        print("Эта функция доступна только на Windows.")
        return

    print("Проверка доступа...")
    if domain_user_block:
        print("У вас нет доступа к этой возможности")
        return

    num = int(input("Вы уверены? (domain user dump) 0/1?:"))
    if num == 1:
        print("Запуск...")
        dud()
        input("Нажмите enter для продолжения...")
    else:
        print("OK")

def tg_tool():
    num = int(input("Вы уверены? (Telegram Tool) 0/1?:"))
    if num == 1:
        print("Запуск...")
        get_API()
        asyncio.run(tgmain())
        int(input("Нажмите enter для продолжения..."))
    else:
        print("OK")

def stress_test():
    num = int(input("Вы уверены? (stress test) 0/1?:"))
    if num == 1:
        print("Запуск...")
        st()
        print("Стресс-тест завершен успешно.")
    else:
        print("OK")

def sshmag():
    num = int(input("Вы уверены? (SSH client) 0/1?:"))
    if num == 1:
        print("Запуск...")
        ssh()
        int(input("Нажмите enter для продолжения..."))
    else:
        print("OK")

def nmap():
    num = int(input("Вы уверены? (Scan Ports) 0/1?:"))
    if num == 1:
        print("Запуск...")
        simple_nmap()
        int(input("Нажмите enter для продолжения..."))
    else:
        print("OK")

def ch_vr():
    num = int(input("Вы уверены? (Scan system) 0/1?:"))
    if num == 1:
        print("Запуск...")
        scan_system()
        int(input("Нажмите enter для продолжения..."))
        print("Сканирование завершено успешно.")
    else:
        print("OK")

def uyaz():
    num = int(input("Вы уверены? (Скан на уязвимости) 0/1?:"))
    if num == 1:
        print("Запуск...")
        nmap_path = r"C:\Program Files (x86)\Nmap"
        os.environ["PATH"] += os.pathsep + nmap_path
        scan_vulnerabilities()
        int(input("Нажмите enter для продолжения..."))
        print("Сканирование завершено успешно.")
    else:
        print("OK")

def betaf():
    from main1 import beta_block  # Переносим импорт сюда, чтобы избежать циклического импорта
    num = int(input("Вы уверены? (Beta Functions) 0/1?:"))
    if num == 1:
        print('Проверка доступа...')
        if beta_block:
            print("У вас нет доступа к этой возможности")
            int(input("Нажмите enter для продолжения..."))
            return
        print("Запуск...")
        beta.main()
        int(input("Нажмите enter для продолжения..."))
        print("Успешный выход из beta func.")
    else:
        print("OK")


functions = [
    {"id": 0, "name": "Настройки", "func": settings},
    {"id": 1, "name": "Dump локальных user", "func": local_user_dump},
    {"id": 2, "name": "Dump /domain", "func": domain_user_dump},
    {"id": 3, "name": "Stress Test", "func": stress_test},
    {"id": 4, "name": "Telegram Tool", "func": tg_tool},
    {"id": 5, "name": "SSH клиент", "func": sshmag},
    {"id": 6, "name": "Скан портов", "func": nmap},
    {"id": 7, "name": "Информация об устройстве", "func": ch_vr},
    {"id": 8, "name": "Скан уяз. linux", "func": uyaz},
    {"id": 9, "name": "Beta func", "func": betaf}
]

def display_functions():
    print("Доступные функции:")
    max_name_length = max(len(f['name']) for f in functions)
    for i, f in enumerate(functions):
        print(f"[{f['id']}] {f['name']:<{max_name_length}}", end="\t")
        if (i + 1) % 4 == 0:
            print()
    print()