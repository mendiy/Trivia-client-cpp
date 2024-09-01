"""EX 2.6 server implementation
   Author: Mendi Yacobovitz
   Date: 28/7/24
   Possible client commands defined in protocol.py
"""

import socket
import protocol
import random
import datetime

def create_server_rsp(cmd: str) -> str:
    """Based on the command, create a proper response"""
    if cmd == "NUMBER":
        return str(random.randint(0, 99))
    if cmd == "hello":
        return "Mendi Server"
    if cmd == "TIME":
        return f"Date & Time: {datetime.datetime.now()}"
    if cmd == "EXIT":
        return "EXIT" 


def check_cmd(data: str) -> bool:
    """Check if the command is defined in the protocol (e.g NUMBER, HELLO, TIME, EXIT)"""
    return data in ["NUMBER", "hello", "TIME", "EXIT"]


def main():
    # Create TCP/IP socket object
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind server socket to IP and Port
    my_socket.bind(("0.0.0.0", protocol.PORT))

    # Listen to incoming connections
    my_socket.listen()

    print("Server is up and running")

    # Create client socket for incoming connection
    client_socket, client_address = my_socket.accept()

    print(f"Client {client_address} connected")

    while True:
        # Get message from socket and check if it is according to protocol
        cmd = protocol.get_msg(client_socket)
        if True:
            # 1. Print received message
            print(cmd)

            # 2. Check if the command is valid, use "check_cmd" function
            if check_cmd(cmd):
                cmd_response = create_server_rsp(cmd)

                # 3. If valid command - create response
                response = cmd_response
            else:
                response = "Wrong protocol"
             
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage

        # Send response to the client
        response = protocol.create_msg(response)
        client_socket.send(response)

        # If EXIT command, break from loop
        if cmd == "EXIT":
            break

    print("Closing\n")

    # Close sockets
    client_socket.close()
    my_socket.close()


if __name__ == "__main__":
    main()
