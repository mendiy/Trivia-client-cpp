import json


LENGTH_FIELD_SIZE = 4
PORT = 8000


def create_msg(data, status=0):
    """Create a valid protocol message, with length field"""
    lenght = len(data)
    message = (status).to_bytes(1, byteorder='big') + len(data).to_bytes(4, byteorder='big') + data.encode("ASCII");
    print(message)
    return message

def get_msg(my_socket):
	id = my_socket.recv(1)
	length = int.from_bytes(my_socket.recv(4), byteorder='big')
	message = ""
	while len(message) < length:
		message += (my_socket.recv(length)).decode("ASCII")
	return id, message

def login_msg():
    user_name = input("user name: ")
    password = input("password: ")
    user_data = {"username" : user_name, "password" : password}
    data = json.dumps(user_data)

    return create_msg(data, 100)

def signin_msg():
    user_name = input("user name: ")
    password = input("password: ")
    email = input("email: ")
    user_data = {"username" : user_name, "password" : password, "email" : email}
    data = json.dumps(user_data)

    return create_msg(data, 101)

