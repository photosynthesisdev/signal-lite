from fastapi import FastAPI, WebSocket, Request
from .database import SimpleMessagingDB
from .models import ServerValidatedMessage
from starlette.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

import logging

app = FastAPI()
app.mount("/", StaticFiles(directory="/root/signal-lite/frontend", html=True), name="frontend")

@app.get("/api/bootup")
def bootup(request : Request):
    return "sup"

@app.websocket("/api/chatConnect")
async def websocket(websocket: WebSocket):
    def watch_callback(self, new_messages : list[ServerValidatedMessage]):
        # As we become aware of new messages from other clients in the database, append those to the json that server should send to the client
        for message in new_messages:
            json_to_send.append(message.json())

    # Accepting websocket connection, this is a standard part of websocket implementations.
    # We may want to do some type of verification/authorization of who is connecting before accepting the connection.
    # However, for the purposes of Signal Lite we will just allow anyone to connect and join the chat room.
    await websocket.accept()
    
    # This creates our database object. See database.py for the internal workings of this.
    # This basicaly allows us to read/write new messages to the chatroom.
    # The watch callback is a method that will get invoked when other clients send messages - this way we can receive realtime updates. 
    database = SimpleMessagingDB('./database/SignalLite.db', watch_callback)

    # A helper list which will contain json strings that the server sends to client. These strings will contain information about new messages.
    json_to_send : list[str] = []
    try:
        while True:
            # While true loop for sending/receiving data
            ...
    except Exception as e:
        logging.error(f"An Exception occured in /chatConnect Websocket: {e}")
    finally:
        database.close_connection()

# statically mount files in /root/signal-lite/frontend
# 