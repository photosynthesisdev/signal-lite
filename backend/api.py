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

class LocalClient(BaseModel):
    local_client_user_id : int
    local_client_username : str

class MessageRecord(BaseModel):
    user_id : int
    username : str
    timestamp : float
    message : str

usernames = ["Bumble", "Zap", "Whisker", "Froodle", "Ziggy", "Snappy", "Fizzle", "Giggle", "Bongo", "Puff", "Doodle","Chomp", "Scooter", "Wobble", "Twizzle", "Zoom", "Quirk", "Flap", "Squish", "Wizzle"]

@router.websocket("/chatConnect")
async def chatConnect(websocket: WebSocket):
    async def send_message_to_client(message: str):
        try:
            await websocket.send_text(message)
        except Exception as e:
            logging.error(f"Error sending message to client: {e}")
    def watch_callback(watch_response):
        for event in watch_response.events:
            if isinstance(event, etcd3.events.PutEvent):
                value = event.value.decode("utf-8")
                asyncio.run_coroutine_threadsafe(send_message_to_client(value), loop)
    await websocket.accept()
    user_id = random.randint(0, 1000000)
    username = f"{random.choice(usernames)}{random.choice(usernames)}{random.randint(0, 99)}"
    await websocket.send_text(
        LocalClient(
            local_client_user_id = user_id,
            local_client_username = username
        ).json()
    )
    loop = asyncio.get_event_loop()
    watch_id = database.add_watch_prefix_callback("/v1/messages", watch_callback)
    json_to_send : list[str] = []
    try:
        while True:
            # Receive Loop.
            message_from_client = (await websocket.receive()).get("text", "")
            message_record = MessageRecord(
                user_id = user_id, 
                username = username, 
                timestamp = time.time(), 
                message = message_from_client
            )
            database.put(f"/v1/messages/{time.time()}", value = message_record.json())
    except Exception as e:
        logging.error(f"An Exception occured in /chatConnect Websocket: {e}")
        try:
            await websocket.close()
        except:
            ...
    finally:
        database.cancel_watch(watch_id)

# This will give us all of our static frontend files (HTML, CSS, JavaScript) so that we can properly render client experience
app.mount("/static", StaticFiles(directory="/root/signal-lite/frontend", html=True), name="frontend")

# This will lead to our API endpoints so we can properly manage backend experience.
app.include_router(router, prefix="/api")