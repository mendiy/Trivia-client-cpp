
import socket
import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
      my_socket.connect(("127.0.0.1", protocol.PORT))

      my_socket.settimeout(5.0)
    except socket.error:
        print("Error! connction failed\n")
        my_socket.close()
  

    while True:
        user_input = input("Enter command (5 bytes):\n")
        # 1. Add length field ("HELLO" -> "04HELLO")
        # 2. Send it to the server

        try:
            my_socket.send(protocol.create_msg(user_input))
        except socket.error:
                #write error code 
            print("Error! sending message failed\n")
            my_socket.close()


        # 3. Get server's response
        try:
            data = protocol.get_msg(my_socket)
        except socket.error:
            print("Error! reciving message failed\n")
            my_socket.close()

        # 4. If server's response is valid, print it
        if data:
            print(data)
      
        # 5. If command is EXIT, break from while loop
        if user_input == "EXIT":
            break

    print("Closing\n")
    # Close socket
    my_socket.close()

    








if __name__ == "__main__":
    main()

