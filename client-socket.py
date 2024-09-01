
import socket

PORT = 8000

def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", PORT))

    while True:
        user_input = input("Enter command\n")

        # 1. Send it to the server
        my_socket.send(user_input.encode())

        # 2. Get server's response
        data = my_socket.recv(1024).decode()

        # 3. If server's response is valid, print it
        if data:
            print(data)
    
        # 4. If command is EXIT, break from while loop
        if user_input == "EXIT":
            break

    print("Closing\n")

    # Close socket
    my_socket.close()


if __name__ == "__main__":
    main()

