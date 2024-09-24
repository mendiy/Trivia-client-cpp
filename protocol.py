import json

##############
### Consts ###
##############

#define ERROR_RESPONSE_CODE 126
#define LOGIN_RESPONSE_CODE 100
#define SIGNUP_RESPONSE_CODE 101
#define LOGOUT_RESPONSE_CODE 101
#define GET_ROOMS_RESPONSE_CODE 20
#define GET_PLAYERS_IN_ROOM_RESPONSE_CODE 30
#define GET_HIGH_SCORE_RESPONSE_CODE 40
#define GET_PERSONAL_STATS_RESPONSE_CODE 50
#define JOIN_ROOM_RESPONSE_CODE 60
#define CREATE_ROOM_RESPONSE_CODE 70
#define CLOSE_RESPONSE_CODE 80
#define START_GAME_RESPONSE_CODE 90
#define GET_ROOM_STATE_RESPONSE_CODE 95
#define LEAVE_ROOM_RESPONSE_CODE 99
#define LEAVE_GAME_RESPONSE_CODE 73
#define GET_QUESTION_RESPONSE_CODE 71
#define SUBMIT_ANSWER_RESPONSE_CODE 72
#define GET_GAME_RESULTS_RESPONSE_CODE 74"

FIRST_ARG_IDX = 1
IP = "127.0.0.1"
PORT = 8000
# Packet Menu Options
LOGIN = 1
SIGNUP = 2
LOGOUT = 3
ENDIANESS = "big"

MESSAGE_CODES = {
    'ERROR': 1,
    'LOG_IN': 2,
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
    message = id + len(string_dic).to_bytes(4, byteorder=ENDIANESS) + string_dic.encode("ASCII")
    while send_from < len(message):
        send_from += sock.send(message[send_from:])


def recv(sock):
    reversed_dic = {value : key for key, value in MESSAGE_CODES.items()}
    id = sock.recv(1)
    id = int.from_bytes(id, byteorder=ENDIANESS)
    # id = ord(id.decode())
    print(f"response code: {reversed_dic.get(id, 'protocol error unexpected code ')} ({id})")
    length = int.from_bytes(sock.recv(4), byteorder=ENDIANESS)
    message = ""
    while len(message) < length:
        message += (sock.recv(length)).decode("ASCII")
    return message, id