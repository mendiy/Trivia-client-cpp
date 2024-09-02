import socket
import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        user_input = input("Enter 'L' to log-in or 'S' to sign-up: ")
        try:
            if user_input == 'L':
                my_socket.send(protocol.login_msg())
            elif user_input == 'S':
                my_socket.send(protocol.signin_msg())
            else:
                my_socket.send(protocol.create_msg)
        
            # 3. Get server's response
        except socket.error:
            print("Error!")

        data = protocol.get_msg(my_socket)
        # 4. If server's response is valid, print it
        if data[0]:
            print(data[1])
      
        # 5. If command is EXIT, break from while loop
        if user_input == "EXIT":
            break

    print("Closing\n")
    # Close socket
    my_socket.close()


if __name__ == "__main__":
    main()

