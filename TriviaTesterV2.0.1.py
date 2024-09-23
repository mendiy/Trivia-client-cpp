import json
import socket
import math
import sys
import os
#import bson

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

#######################
### Message Related ###
#######################

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
    print(f"response code: {reversed_dic.get(id, "protocol error unexpected code ")} ({id})")
    length = int.from_bytes(sock.recv(4), byteorder=ENDIANESS)
    message = ""
    while len(message) < length:
        message += (sock.recv(length)).decode("ASCII")
    return message, id


def signup(sock):
    ##### Mandatory user attributes ####
    username = input("Enter username: ")
    password = input("Enter password: ")
    email = input("Enter email: ")

    message_dict = {
        "username": username,
        "password": password,
        "email": email
    }

    send(sock, MESSAGE_CODES["SIGN_UP"], message_dict)


def login(sock):
    ##### Mandatory user attributes ####
    username = input("Enter username: ")
    password = input("Enter password: ")

    message_dict = {
        "username": username,
        "password": password
    }

    send(sock, MESSAGE_CODES["SIGN_IN"], message_dict)


def handle_server_response(sock):
    # Receive the initial response from the server
    response, code = recv(sock)
    if(code == MESSAGE_CODES["ERROR"]):
        print("login or signup failed, return code was ", code)
        return 
    response_json = json.loads(response)
    print(response_json)

    # Check if the login or signup was successful
    # if status_code == 100:
    #     print("Login successful!")
    # elif status_code == 101:
    #     print("Signup successful!")
    # else:
    #     print("Login/Signup failed with status code:", status_code)
    #     return

    # Show the menu if login/signup was successful
    while True:
        print("\nMenu:")
        print("1. Get Rooms")
        print("2. Create Room")
        print("3. Logout")
        print("4. Join Room")
        print("5. Get Players in Room")
        print("6. Get High Scores")
        print("7. Get Personal Stats")
        print("8. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 8.")
            continue

        if choice == 1:
            send(sock, MESSAGE_CODES["GET_ROOMS"])
        elif choice == 2:
            room_name = input("Enter room name: ")
            try:
                max_users = int(input("Enter maximum number of users: "))
                answer_timeout = int(input("Enter answer timeout in seconds: "))
                question_count = int(input("Enter question count: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            send(sock, MESSAGE_CODES["CREATE_ROOM"], {
                "roomName": room_name,
                "maxUsers": max_users,
                "answerTimeout": answer_timeout,
                "questionCount": question_count
            })
        elif choice == 3:
            send(sock, MESSAGE_CODES["SIGN_OUT"])
            handle_server_response(sock)
            print("Logged out.")
            break
        elif choice == 4:
            room_id = input("Enter room ID: ")
            send(sock, MESSAGE_CODES["JOIN_ROOM"], {"roomId": room_id})
        elif choice == 5:
            room_id = input("Enter room ID: ")
            send(sock, MESSAGE_CODES["GET_PLAYERS_IN_ROOM"], {"roomId": room_id})
        elif choice == 6:
            send(sock, MESSAGE_CODES["HIGH_SCORE"])
        elif choice == 7:
            send(sock, MESSAGE_CODES["PERSONAL_STATS"])
        elif choice == 8:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

        response, code = recv(sock)
        response_json = json.loads(response)
        print(response_json)


# Example integration (after signup or login)
def example_login_flow(sock):
    login(sock)
    handle_server_response(sock)


def example_signup_flow(sock):
    signup(sock)
    handle_server_response(sock)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, PORT))  # Replace with your server's IP and port
example_login_flow(sock)
