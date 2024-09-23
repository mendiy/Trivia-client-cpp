from fastapi import FastAPI
import socket
import protocol
from pydantic import BaseModel

class Item(BaseModel):
    username: str | None = None,
    password: str | None = None,
    email: str | None = None,

class Room(BaseModel):
    room_name: str
    max_users: int
    answer_timeout: float
    question_count: int

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((protocol.IP, protocol.PORT))

app = FastAPI()
print("http server running...")

@app.post("/Log-In")
async def login(body: Item):
    body.dict()
    message_dict = {
        "username": body.username,
        "password": body.password,
    }
    protocol.send(my_socket, protocol.MESSAGE_CODES["LOG_IN"], message_dict)
    response, code = protocol.recv(my_socket)
    return  response, code

@app.post("/Sign-In")
async def signin(body: Item):
    protocol.send(my_socket, protocol.MESSAGE_CODES["SIGN_UP"], body.dict())
    response, code = protocol.recv(my_socket)
    return  response, code

@app.get("/Get-Rooms")
async def get_rooms():
    protocol.send(my_socket, protocol.MESSAGE_CODES["GET_ROOMS"])
    response, code = protocol.recv(my_socket)
    return  response, code

@app.post("/Create-Room")
async def create_room(body: Room):
    protocol.send(my_socket, protocol.MESSAGE_CODES["CREATE_ROOM"], body.dict())
    response, code = protocol.recv(my_socket)
    return  response, code

@app.get("/Logout")
async def logout():
    protocol.send(my_socket, protocol.MESSAGE_CODES["SIGN_OUT"])
    response, code = protocol.recv(my_socket)
    return  response, code

@app.get("/Join-Room")
async def join_room(room_id : int):
    protocol.send(my_socket, protocol.MESSAGE_CODES["JOIN_ROOM"], {room_id: room_id})
    response, code = protocol.recv(my_socket)
    return  response, code

@app.get("/Get-Players-in-Room")
async def get_players(room_id : int):
    protocol.send(my_socket, protocol.MESSAGE_CODES["GET_PLAYERS_IN_ROOM"], {room_id: room_id})
    response, code = protocol.recv(my_socket)
    return  response, code

@app.get("/Get-High-Scores")
async def get_scores():
    protocol.send(my_socket, protocol.MESSAGE_CODES["HIGH_SCORE"])
    response, code = protocol.recv(my_socket)
    return  response, code

@app.get("/Get-Personal-Stats")
async def get_stats(user_id : int):
    protocol.send(my_socket, protocol.MESSAGE_CODES["PERSONAL_STATS"], {user_id: user_id})
    response, code = protocol.recv(my_socket)
    return  response, code
