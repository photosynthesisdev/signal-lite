from fastapi import FastAPI, WebSocket, Request, APIRouter
from .models import ServerValidatedMessage
from starlette.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
import etcd3
import logging

database = etcd3.client()
app = FastAPI()
router = APIRouter()

@router.websocket("/chatConnect")
async def chatConnect(websocket: WebSocket):
    def watch_callback(self, new_messages : list[ServerValidatedMessage]):
        # As we become aware of new messages from other clients in the database, append those to the json that server should send to the client
        for message in new_messages:
            json_to_send.append(message.json())
    
    # Accepting websocket connection, this is a standard part of websocket implementations.
    # We may want to do some type of verification/authorization of who is connecting before accepting the connection.
    # However, for the purposes of Signal Lite we will just allow anyone to connect and join the chat room.
    await websocket.accept()
    # A helper list which will contain json strings that the server sends to client. These strings will contain information about new messages.
    json_to_send : list[str] = []
    try:
        # while True:
        ...
    except Exception as e:
        try:
            # Close websocket if any issues.
            await websocket.close()
        except Exception as e:
            # we may get caught here if websocket is already closed.
            ...
        logging.error(f"An Exception occured in /chatConnect Websocket: {e}")
    finally:
        database.close_connection()

# This will give us all of our static frontend files (HTML, CSS, JavaScript) so that we can properly render client experience
app.mount("/static", StaticFiles(directory="/root/signal-lite/frontend", html=True), name="frontend")

# This will lead to our API endpoints so we can properly manage backend experience.
app.include_router(router, prefix="/api")