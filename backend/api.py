from fastapi import FastAPI, WebSocket, Request, APIRouter
from starlette.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import etcd3
import logging
import random
import time
import asyncio

database = etcd3.client()
app = FastAPI()
router = APIRouter()

# ---- Models used to communicate data to clients ----

class LocalClient(BaseModel):
    """Data sent to the client the moment that their websocket connection is successfully established. Informs client of their user id."""
    local_client_user_id : int

class MessageRecord(BaseModel):
    """This is a general 'message' object, which contains a record of a message that was sent in the chat. Stored in database."""
    user_id : int
    timestamp : float
    message : str

@router.websocket("/chatConnect")
async def chatConnect(websocket: WebSocket):
    async def send_message_to_client(message_record: str):
        # Basically ignore this. All you need to know is that it sends a messasge record to  our client.
        try:
            await websocket.send_text(message_record)
        except Exception as e:
            logging.error(f"Error sending message to client: {e}")
    def watch_callback(watch_response):
        for event in watch_response.events:
            if isinstance(event, etcd3.events.PutEvent):
                # 'value' is the MessageRecord that was just written to the database.
                value = event.value.decode("utf-8")
                # Ignore this largely, not relevant to discussion of websockets. 
                # In short, it's just a thread safe way to send message to clients b/c 'watch_callback' is a synchronous function.
                asyncio.run_coroutine_threadsafe(send_message_to_client(value), loop)
    
    # --- ACCEPT ANY INCOMING CONNECTION ---
    # If you view 'frontend/main.js', you can see that as soon as the site loads for the client, they establish a connection to "wss://signallite.io/api/chatConnect"
    await websocket.accept()

    # ---- CREATE & SEND USER ID -----
    # The server selects a random user_id for the client to identify themselves as.
    # This ID does not persist between sessions, so every time a client refreshes the page (and connects to this websocket) they will receive a new user_id.
    user_id = random.randint(0, 1000000)
    local_client_json_string = LocalClient(local_client_user_id = user_id).json()
    await websocket.send_text(local_client_json_string)


    # ---- SEND OLD CHAT MESSAGE RECORDS TO CLIENT -----
    # This goes to the database key "/v1/messages" and gets all old messages sent in the chat before this user came to the website.
    old_message_data = database.get_prefix("/v1/messages")
    for old_message in old_message_data:
        msg = old_message[0].decode('utf-8')
        await websocket.send_text(msg)

    
    # ---- LISTEN FOR NEW MESSAGES -----
    # Over the lifespan of this connection, we want to ensure any new messages sent by clients are broadcasted to all other clients.
    # We do this via the notion of a 'watch' which looks at a key prefix, and sends updates.
    loop = asyncio.get_event_loop()
    watch_id = database.add_watch_prefix_callback("/v1/messages", watch_callback)


    # -------- WHILE TRUE RECEIVE LOOP --------
    # This keeps the websocket connection alive for the duration of the clients connection.
    # When the client disconnects (closes the tab), a WebSocket exception will be raised, hence why we have the try/except block.
    try:
        while True:
            # Listen for any new messages that this client has sent.
            message_from_client = (await websocket.receive()).get("text", "")
            # Once the client sends a message, create a MessageRecord object, and store it in the database.
            message_record = MessageRecord(
                user_id = user_id, 
                username = username, 
                timestamp = time.time(), 
                message = message_from_client
            )
            # Once we store this in the database, it will notify all users connected to the websocket that a new piece of message was sent to the database.
            database.put(f"/v1/messages/{time.time()}", value = message_record.json())
    except Exception as e:
        try:
            await websocket.close()
        except:
            pass
    finally:
        database.cancel_watch(watch_id)

@router.get("/deleteChatHistory")
def deleteChatHistory():
    """ Deletes old chat history. We wouldn't keep this in a production enviroment, but is useful to clear out old messages. """
    database.delete_prefix("/v1/messages")
    return {"success": True}

# Mounts static files to be send over API. This is all frontend files, so HTML/JS/CSS
app.mount("/static", StaticFiles(directory="/root/signal-lite/frontend", html=True), name="frontend")
# Mounts api endpoints, which is just chatConnect & deleteChatHistory
app.include_router(router, prefix="/api")