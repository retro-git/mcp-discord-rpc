from pypresence import Presence
import time, os
import urllib.request, json
import configparser

configParser = configparser.ConfigParser()
configParser.read(os.getcwd() + "//config.txt")
addr = "http://" + configParser.get('config', 'mcp_local_ip') + "/api/currentState"
client_id = configParser.get('config', 'client_id')
refresh_delay = int(configParser.get('config', 'refresh_delay'))
wait_on_fail = int(configParser.get('config', 'wait_on_fail'))
default_image = configParser.get('config', 'default_image')
RPC = Presence(client_id, pipe=0)
RPC.connect()

while True:
    try:
        prevGameData = json.loads(urllib.request.urlopen(addr).read().decode())
        prevGameName = prevGameData['gameName']
        prevGameID = prevGameData['gameID'].lower()
        starttime = time.time()
        status = RPC.update(details=prevGameName, start=starttime, large_image=prevGameID)
        if not status['data']['assets']:
            status = RPC.update(details=prevGameName, start=starttime, large_image=default_image)

        print(status)

        while True:
            time.sleep(refresh_delay)
            curGameData = json.loads(urllib.request.urlopen(addr).read().decode())
            curGameName = curGameData['gameName']
            if prevGameName != curGameName:
                prevGameName = curGameName
                prevGameID = curGameData['gameID'].lower()
                starttime = time.time()
                status = RPC.update(details=prevGameName, start=starttime, large_image=prevGameID)
                if not status['data']['assets']:
                    status = RPC.update(details=prevGameName, start=starttime, large_image=default_image)

                print(status)
    except:
        print('Connection failed, trying again in ' + str(wait_on_fail/60) + ' minutes');
        time.sleep(wait_on_fail)

