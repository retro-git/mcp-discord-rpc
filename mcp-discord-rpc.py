from pypresence import Presence
import time
import urllib.request, json

client_id = '833541435281375273'
RPC = Presence(client_id, pipe=0)
RPC.connect()

prevGameName = json.loads(urllib.request.urlopen("http://192.168.0.31/api/currentState").read().decode())['gameName']
prevGameID = json.loads(urllib.request.urlopen("http://192.168.0.31/api/currentState").read().decode())['gameID'].lower()
starttime = time.time()
print(RPC.update(details=prevGameName, start=starttime, large_image=prevGameID))

while True:
    time.sleep(5)
    curGameName = json.loads(urllib.request.urlopen("http://192.168.0.31/api/currentState").read().decode())['gameName']
    curGameID = json.loads(urllib.request.urlopen("http://192.168.0.31/api/currentState").read().decode())['gameID'].lower()
    if prevGameName != curGameName:
        prevGameName = curGameName
        prevGameID = curGameID
        starttime = time.time()
        print(RPC.update(details=prevGameName, start=starttime, large_image=prevGameID))

