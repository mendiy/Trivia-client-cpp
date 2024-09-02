import json


LENGTH_FIELD_SIZE = 4
PORT = 8000



def create_msg(data, status=0):
    """Create a valid protocol message, with length field"""
    lenght = len(data)
    message = (status).to_bytes(1, byteorder='big') + len(data).to_bytes(4, byteorder='big') + data.encode("ASCII");
    #print(message)
    return message

def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    message_len = my_socket.recv(4).decode()

    if str(message_len).isdigit() == False:
        return False, "Error"
    
    message = my_socket.recv(int(message_len)).decode()

    return True ,message

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
