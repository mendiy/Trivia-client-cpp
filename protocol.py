
# LENGTH_FIELD_SIZE = 2
PORT = 8000

def create_msg(data):
    return data.encode()


def get_msg(my_socket):
    message = my_socket.recv(1024).decode()
    return message


# def create_msg(data):
#     """Create a valid protocol message, with length field"""
#     lenght = len(data)
#     field_lenght = str(lenght).zfill(LENGTH_FIELD_SIZE)
#     return (field_lenght + data).encode()

# def get_msg(my_socket):
#     """Extract message from protocol, without the length field
#        If length field does not include a number, returns False, "Error" """
#     message_len = my_socket.recv(LENGTH_FIELD_SIZE).decode()

#     if str(message_len).isdigit() == False:
#         return False, "Error"
    
#     message = my_socket.recv(int(message_len)).decode()

#     return True, message
