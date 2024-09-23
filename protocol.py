import json

##############
### Consts ###
##############

FIRST_ARG_IDX = 1
IP = "127.0.0.1"
PORT = 8888
# Packet Menu Options
LOGIN = 1
SIGNUP = 2
LOGOUT = 3
ENDIANESS = "little"

MESSAGE_CODES = {
    'ERROR': 1,
    'SIGN_IN': 2,
    'SIGN_UP': 3,
    'SIGN_OUT': 5,
    'GET_ROOMS': 7,
    'GET_PLAYERS_IN_ROOM': 11,
    'JOIN_ROOM': 13,
    'CREATE_ROOM': 17,
    'HIGH_SCORE': 19,
    'PERSONAL_STATS': 23,
    'SUCCESS_STATS': 16
 }


def send(sock, req_id, dict={}):
    send_from = 0
    string_dic = ""
    if dict is not {}:
        string_dic = json.dumps(dict)
    # print("Enter the message code (1 Byte): ")
    id = req_id.to_bytes(1, byteorder=ENDIANESS)
    message = id + len(string_dic).to_bytes(4, byteorder=ENDIANESS) + string_dic.encode("ASCII");
    while send_from < len(message):
        send_from += sock.send(message[send_from:])


def recv(sock):
    reversed_dic = {value : key for key, value in MESSAGE_CODES.items()}
    id = sock.recv(1)
    id = int.from_bytes(id)
    # id = ord(id.decode())
    print(f"response code: {reversed_dic.get(id, 'protocol error unexpected code ')} ({id})")
    length = int.from_bytes(sock.recv(4), byteorder=ENDIANESS)
    message = ""
    while len(message) < length:
        message += (sock.recv(length)).decode("ASCII")
    return message, id