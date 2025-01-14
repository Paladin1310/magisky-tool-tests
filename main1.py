import datetime
import importlib
import socket
import subprocess
import sys
import logging
import os
import asyncio
import threading
import paramiko
import telethon
import json
import platform
from colorama import Fore
from telethon.sync import TelegramClient, events
from tqdm import tqdm
import nmap

from utils import check_key, get_API, restart_program
from function_definitions import settings, local_user_dump, domain_user_dump, tg_tool, stress_test, sshmag, nmap, ch_vr, uyaz, betaf

key_info = check_key()

if "school" in key_info["tags"]:
    print("Ограничение доступа к domain_user_dump")
    domain_user_block = True
else:
    domain_user_block = False

if "guest" in key_info["tags"]:
    print("Ограничение доступа guest")
    domain_user_block = True
    user_guest = True
else:
    domain_user_block = False
    user_guest = False

if "beta" in key_info["tags"]:
    beta_block =  False
else:
    print("Ограничение доступа к beta func")
    beta_block = True

def menu():
    print(Fore.BLUE + "=" * 125)
    print(Fore.BLUE + r"""
 ___      ___       __       _______   __      ________  __   ___  ___  ___      ___________  ______      ______    ___
|"  \    /"  |     /""\     /" _   "| |" \    /"       )|/"| /  ")|"  \/"  |    ("     _   ")/    " \    /    " \  |"  |
 \   \  //   |    /    \   (: ( \___) ||  |  (:   \___/ (: |/   /  \   \  /      )__/  \\__/// ____  \  // ____  \ ||  |
 /\\  \/.    |   /' /\  \   \/ \      |:  |   \___  \   |    __/    \\  \/          \\_ /  /  /    ) :)/  /    ) :)|:  |
|: \.        |  //  __'  \  //  \ ___ |.  |    __/  \\  (// _  \    /   /           |.  | (: (____/ //(: (____/ //  \  |___
|.  \    /:  | /   /  \\  \(:   _(  _|/\  |\  /" \   :) |: | \  \  /   /            \:  |  \        /  \        /  ( \_|:  \
|___|\__/|___|(___/    \___)\_______)(__\_|_)(_______/  (__|  \__)|___/              \__|   \"_____/    \"_____/    \_______)
""")
    print(Fore.BLUE + "=" * 125)
    if "school" in key_info["tags"]:
        print("Ограничение доступа к domain_user_dump")

    functions = [
        {"id": 0, "name": "Настройки", "func": settings},
        {"id": 1, "name": "Dump локальных user", "func": local_user_dump},
        {"id": 2, "name": "Dump /domain", "func": lambda: domain_user_dump(domain_user_block)},
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

    display_functions()

    # Main loop
    while True:
        try:
            user_input = int(input("Введите ID функции для выполнения (или -1 для выхода): "))
            if user_input == -1:
                break

            selected_function = next((f for f in functions if f["id"] == user_input), None)
            if selected_function:
                selected_function["func"]()
            else:
                print("Некорректный ID функции.")
        except ValueError:
            print("Пожалуйста, введите корректный ID.")

if __name__ == "__main__":
    menu()