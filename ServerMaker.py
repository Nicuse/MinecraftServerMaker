# PLEASE DO NOT COPY AND MARK AS YOUR OWN.
# PLEASE GIVE CREDITS IF YOU MODIFY.

import os
import sys
from colorama import *
from PIL import Image
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil
import subprocess
import tempfile
import time
from urllib.parse import urlparse
from tqdm import tqdm
import psutil
import requests
init()

script_dir = os.path.dirname(sys.executable)
serv_prop = {
    "enable-jmx-monitoring": "false",
    "rcon.port": "25575",
    "level-seed": "",
    "gamemode": "survival",
    "enable-command-block": "true",
    "enable-query": "false",
    "generator-settings": "{}",
    "enforce-secure-profile": "true",
    "level-name": "world",
    "motd": "A Minecraft Server",
    "query.port": "25565",
    "pvp": "true",
    "generate-structures": "true",
    "max-chained-neighbor-updates": "1000000",
    "difficulty": "easy",
    "network-compression-threshold": "256",
    "max-tick-time": "60000",
    "require-resource-pack": "false",
    "max-players": "20",
    "use-native-transport": "true",
    "online-mode": "false",
    "enable-status": "true",
    "allow-flight": "false",
    "initial-disabled-packs": "",
    "broadcast-rcon-to-ops": "true",
    "view-distance": "10",
    "resource-pack-prompt": "",
    "server-ip": "",
    "allow-nether": "true",
    "server-port": "25565",
    "enable-rcon": "false",
    "sync-chunk-writes": "true",
    "resource-pack-id": "",
    "op-permission-level": "4",
    "prevent-proxy-connections": "false",
    "hide-online-players": "false",
    "resource-pack": "",
    "entity-broadcast-range-percentage": "100",
    "simulation-distance": "10",
    "rcon.password": "",
    "player-idle-timeout": "0",
    "force-gamemode": "false",
    "rate-limit": "0",
    "debug": "false",
    "hardcore": "false",
    "white-list": "false",
    "broadcast-console-to-ops": "true",
    "spawn-npcs": "true",
    "spawn-animals": "true",
    "log-ips": "true",
    "function-permission-level": "2",
    "initial-enabled-packs": "vanilla",
    "level-type": "minecraft:normal",
    "text-filtering-config": "",
    "spawn-monsters": "true",
    "enforce-whitelist": "false",
    "spawn-protection": "0",
    "resource-pack-sha1": "",
    "max-world-size": "29999984"
}

def info(any):
    print(f"{Fore.LIGHTBLACK_EX}[Info] {any}")

print((Fore.GREEN + """
  __  __ _                            __ _      _____                            __  __       _             
 |  \/  (_)                          / _| |    / ____|                          |  \/  |     | |            
 | \  / |_ _ __   ___  ___ _ __ __ _| |_| |_  | (___   ___ _ ____   _____ _ __  | \  / | __ _| | _____ _ __ 
 | |\/| | | '_ \ / _ \/ __| '__/ _` |  _| __|  \___ \ / _ \ '__\ \ / / _ \ '__| | |\/| |/ _` | |/ / _ \ '__|
 | |  | | | | | |  __/ (__| | | (_| | | | |_   ____) |  __/ |   \ V /  __/ |    | |  | | (_| |   <  __/ |   
 |_|  |_|_|_| |_|\___|\___|_|  \__,_|_|  \__| |_____/ \___|_|    \_/ \___|_|    |_|  |_|\__,_|_|\_\___|_|   
                                                                                                            
                                                                                                            
"""))

info("Checking Java is installed...")

def OpenFile(url):
    temp_dir = tempfile.mkdtemp()
    filename = os.path.basename(urlparse(url).path)
    file_path = os.path.join(temp_dir, filename)
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
        with open(file_path, "wb") as f:
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                progress_bar.update(len(data))
        progress_bar.close()
        subprocess.Popen([file_path])
        while True:
            if not any(p.name() == filename for p in psutil.process_iter()):
                break
            time.sleep(1)
    else:
        print("Failed to download Java.")

VERSION_SELECTED = "0.0.0"

def InstallVersion(version):
    global VERSION_SELECTED
    VERSION_SELECTED = version
    url = f"https://serverjars.com/api/fetchJar/vanilla/vanilla/{version}"
    response = requests.get(url, stream=True)
    if response.status_code == 404:
        raise ValueError("Invalid version.")
        return
    filename = os.path.basename(urlparse(url).path)
    file_path = os.path.join(server_path, f"{filename}.jar")

    if response.status_code == 200:
        total_size = int(response.headers.get('content_length', 0))
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
        with open(file_path, "wb") as f:
            for data in response.iter_content(chunk_size=1024):
                f.write(data)
                progress_bar.update(len(data))
        progress_bar.close()

def AskForJava():
    while True:
        boolean = input(f"{Fore.WHITE}Java is not detected. It is required for running the server. Install it? (y/n)\n")
        if boolean == "y":
            info("Attempting to install Java SDK 17...")
            OpenFile("https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe")
            break
        elif boolean == "n":
            break
        else:
            print("Please choose a option from y/n!")

try:
    result = subprocess.run(['java', '-version'], capture_output=True, text=True)
    output = result.stderr

    if "java version" in output.lower():
        info("Java is already installed!")
    else:
        AskForJava()
except FileNotFoundError:
    AskForJava()

def boolean(any, key):
    while True:
        boolean_input = input(f"{Fore.WHITE}{any} (y/n):\n")
        if boolean_input == "y":
            serv_prop[key] = True
            break
        elif boolean_input == "n":
            serv_prop[key] = False
            break
        else:
            print("Invalid answer! Please choose from y/n!")

server_name = input(f"{Fore.WHITE}Enter server name:\n")
server_dir = filedialog.askdirectory(title="Select server location")
server_path = os.path.join(server_dir, server_name)
if not os.path.exists(server_path):
    os.mkdir(server_path)

def AskForVersion():
    server_version = input(f"{Fore.WHITE}Please select server version (e.g. 1.16.5, 1.20): ")
    try:
        print("Installing server version...")
        InstallVersion(server_version)
    except:
        print("Invalid version!")
        AskForVersion()

AskForVersion()

while True:
    world_type = input(f"{Fore.WHITE}World Type: (1=Normal, 2=Superflat, 3=Large Biomes, 4=Amplified)\n")
    if world_type in ['1', '2', '3', '4']:
        break
    else:
        print("Invalid world type! Please choose from 1, 2, 3, or 4.")

serv_prop["level-type"] = {
    '1': "minecraft:normal",
    '2': "minecraft:flat",
    '3': "minecraft:largeBiomes",
}.get(world_type, "minecraft:amplified")

boolean("Hardcore", "hardcore")

if serv_prop["hardcore"] == False:
    while True:
        difficulty = input(f"{Fore.WHITE}Difficulty: (1=Easy, 2=Normal, 3=Hard)\n")
        if world_type in ['1', '2', '3']:
            break
        else:
            print("Invalid world type! Please choose from 1, 2, 3, or 4.")

    serv_prop["difficulty"] = {
        '1': "easy",
        '2': "normal",
        '3': "hard",
    }.get(world_type, "normal")

boolean("Online Mode (Allow Only Premium Account Users)", "online-mode")

server_description = input(f"{Fore.WHITE}Enter server description: ")
if server_description != "":
    serv_prop["motd"] = server_description

def downscale_image(image_path):
    try:
        image = Image.open(image_path)
        downscaled_image = image.resize((64, 64))
        downscaled_image.save(f"{server_path}/server-icon.png")
    except:
        print("Could not downscale image")
        

def prompt_user():
    try:
        root = Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select an image file")
        if file_path:
            downscale_image(file_path)
    except:
        print("Could not prompt for icon!")
while True:
    boolean_input = input(f"{Fore.WHITE}Do you want to set a icon for the server (y/n):\n")
    if boolean_input == "y":
        prompt_user()
        break
    elif boolean_input == "n":
        break
    else:
        print("Invalid answer! Please choose from y/n!")

while True:
    MAX_PLAYERS = input(f"{Fore.WHITE}Maximum players:\n")
    if MAX_PLAYERS.isdigit():
        serv_prop["max-players"] = str(int(MAX_PLAYERS))
        break
    else:
        print("Invalid answer! Please enter a number.")

boolean("Spawn Monsters", serv_prop["spawn-monsters"])
boolean("Spawn NPCs", serv_prop["spawn-npcs"])
boolean("Spawn Animals", serv_prop["spawn-animals"])

info("Agreeing to EULA...")
with open(f"{server_path}/eula.txt", 'w') as f:
    f.write("eula=true")
info("Making server.properties")
with open(f"{server_path}/server.properties", 'w') as f:
    f.write('\n'.join(f"{key}={value}" for key, value in serv_prop.items() if value))
info("Making start file")
with open(f"{server_path}/START SERVER.bat", 'w') as f:
    f.write(f"java -Xmx{int((psutil.virtual_memory().total / (1024 * 1024))/8)}M -Xms{int((psutil.virtual_memory().total / (1024 * 1024))/8)}M -jar {VERSION_SELECTED}.jar nogui")
