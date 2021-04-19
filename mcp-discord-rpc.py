from pypresence import Presence
import time
import urllib.request, json

client_id = '833541435281375273'  # Fake ID, put your real one here
RPC = Presence(client_id, pipe=0)  # Initialize the client class
RPC.connect() # Start the handshake loop

prevGameName = json.loads(urllib.request.urlopen("http://192.168.0.31/api/currentState").read().decode())['gameName']
starttime = time.time()
print(RPC.update(details=prevGameName, start=starttime))  # Set the presence

while True:  # The presence will stay on as long as the program is running
    time.sleep(5) # Can only update rich presence every 5 seconds
    curGameName = json.loads(urllib.request.urlopen("http://192.168.0.31/api/currentState").read().decode())['gameName']
    if prevGameName != curGameName:
        prevGameName = curGameName
        starttime = time.time()
        print(RPC.update(details=prevGameName, start=starttime))

