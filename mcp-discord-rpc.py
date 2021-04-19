from pypresence import Presence
import time, os
import urllib.request, json
import configparser

configParser = configparser.ConfigParser()
configParser.read(os.getcwd() + "//config.txt")
addr = "http://" + configParser.get('config', 'mcp_local_ip') + "/api/currentState"
client_id = '833541435281375273'
RPC = Presence(client_id, pipe=0)
RPC.connect()

prevGameName = json.loads(urllib.request.urlopen(addr).read().decode())['gameName']
prevGameID = json.loads(urllib.request.urlopen(addr).read().decode())['gameID'].lower()
starttime = time.time()
print(RPC.update(details=prevGameName, start=starttime, large_image=prevGameID))

while True:
    time.sleep(5)
    curGameName = json.loads(urllib.request.urlopen(addr).read().decode())['gameName']
    if prevGameName != curGameName:
        prevGameName = curGameName
        prevGameID = json.loads(urllib.request.urlopen(addr).read().decode())['gameID'].lower()
        starttime = time.time()
        print(RPC.update(details=prevGameName, start=starttime, large_image=prevGameID))

