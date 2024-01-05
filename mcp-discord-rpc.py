from pypresence import Presence
import time
import os
import urllib.request
import json
import configparser

configParser = configparser.ConfigParser()
configParser.read(os.getcwd() + "//config.txt")

# Read system and mcp_local_ip from the configuration file
system_option = configParser.get('config', 'system')
mcp_local_ip_option = f'mcp_{system_option.lower()}_local_ip' if system_option else 'mcp_local_ip'

addr = "http://" + configParser.get('config', mcp_local_ip_option) + "/api/currentState"
client_id = configParser.get('config', 'client_id')
refresh_delay = int(configParser.get('config', 'refresh_delay'))
wait_on_fail = int(configParser.get('config', 'wait_on_fail'))
default_image = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQMCGQuZ9S4nvzM2xWYD7dzchCZP-ybJiGlv_WTOXaCQ&s'

RPC = Presence(client_id, pipe=0)
RPC.connect()

def generate_large_image_url(system, game_id):
    # Construct the URL based on the specified system and the uppercase version of game_id
    if system.lower() == 'ps2':
        return f'https://raw.githubusercontent.com/xlenore/ps2-covers/main/covers/default/{game_id.upper()}.jpg'
    elif system.lower() == 'ps1':
        return f'https://github.com/xlenore/psx-covers/blob/main/covers/default/{game_id.upper()}.jpg'
    elif system.lower() == 'gcn':
        # Remove the last two characters for 'gcn'
        return f'https://ia801900.us.archive.org/20/items/coversdb-gc/{game_id[:-2].upper()}.png'
    else:
        # Default to the PS2 URL if the system is not recognized
        return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQMCGQuZ9S4nvzM2xWYD7dzchCZP-ybJiGlv_WTOXaCQ&s'

def is_valid_image(url):
    try:
        response = urllib.request.urlopen(url)
        code = response.getcode()
        print(f'Image check for {url}: HTTP Code {code}')
        return code == 200
    except Exception as e:
        print(f'Image check for {url} failed with error: {e}')
        return False

def update_presence(game_data):
    game_name = game_data['gameName']
    game_id = game_data['gameID']
    large_image_url = generate_large_image_url(system_option, game_id)
    
    if not is_valid_image(large_image_url):
        # Use default image URL if the specified one is not available or invalid
        large_image_url = default_image
        print(f'Falling back to default image for game ID: {game_id}')
    
    start_time = time.time()
    status = RPC.update(details=game_name, start=start_time, large_image=large_image_url)
    print(status)

while True:
    try:
        prev_game_data = json.loads(urllib.request.urlopen(addr).read().decode())
        update_presence(prev_game_data)

        while True:
            time.sleep(refresh_delay)
            cur_game_data = json.loads(urllib.request.urlopen(addr).read().decode())
            if prev_game_data['gameName'] != cur_game_data['gameName']:
                prev_game_data = cur_game_data
                update_presence(prev_game_data)
    except Exception as e:
        print(f'Connection failed: {e}. Trying again in {wait_on_fail/60} minutes')
        time.sleep(wait_on_fail)
