from pydantic import BaseModel

class ClientMessageRequest(BaseModel):
    # We don't inclue username/timestamp fields here because the server will manually inject those fields
    # based on the client connection
    message : str

class ServerValidatedMessage(BaseModel):
    username : str
    timestamp : float
    message : str