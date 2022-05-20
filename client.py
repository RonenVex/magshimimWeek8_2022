import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 1234


def print_options():
    """
    The following function will print the options available for the user
    :return: None
    """
    print("""Choose one of the few options:
    ------------------------------
    1) The list of albums
    2) The list of songs in a certain album
    3) The length of a certain song
    4) The lyrics of a certain song
    5) The origin album of a certain song
    6) Searching for a song by it's name
    7) Searching for a song by it's lyrics
    8) Quit""")


def request():
    """
    The following function will handle the conversation with the server thus asking for 
    input from the user
    :return: None
    """
    quitting = False
    with socket.socket() as sock:
        server_address = (SERVER_IP, SERVER_PORT)
        try:
            sock.connect(server_address)
        except Exception as e:
            print("Connection to server failed")
        server_msg = sock.recv(1024)
        print(server_msg.decode())
        while not quitting :
            print_options()
            option = int(input("Enter the option you choose: "))

            while option < 1 or option > 8: #Input Checking
                print("Invalid input, try again")
                option = int(input("Enter the option you choose: "))
            
            msg = "ASK_FUNCTION:{" + str(option * 10) + "}"

            if option > 1 and option < 8:
                asking = ""
                if option == 2:
                    asking = "Enter the name of the album: "
                elif option >= 3 and option <= 5:
                    asking = "Enter the name of the song: "
                elif option == 6:
                    asking = "Enter the word you'd like to search: "
                album_name = input(asking)
                msg += "#additional_data:{" + album_name + "}"

            print() # An empty line

            sock.sendall(msg.encode())
            server_msg = sock.recv(1024)
            # print(server_msg.decode())
            
            server_msg = server_msg.decode()
            
            if option == 8:
                quitting = True

            else:
                printBack(server_msg, option)


def printBack(message, option):
    """
    The following function will print the right message back to the user
    based on the the option and the message sent by the server
    :param message: the message sent by the server
    :type message: string
    :param option: the option that was chosen by the user
    :type option: int
    :return: None
    """
    if "SEND_ALBUMS_LIST" in message:
        print(message.split("{")[1][:-1])

    elif "SEND_ALBUM" in message:
        if option == 2:
            print(message.split("#songs_list:{")[1][:-1])
        elif option == 5:
            print(message.split("SEND_ALBUM:{")[1].split("}")[0])

    elif "SEND_SONGS_LIST" in message:
        print(message.split("SEND_SONGS_LIST:{")[1][:-1].replace(",", "\n"))

    elif "SEND_SONG" in message:
        if option == 3:
            print(message.split("#song_length:{")[1].split("}")[0])
        elif option == 4:
            print(message.split("#song_lyrics:{")[1][:-1])

    else:
        print(message)


def main():
    request()

if __name__ == "__main__":
    main()
