import socket
import data

LISTENING_PORT = 1234
SERVER_IP = "127.0.0.1"

def conversation():
    """
    The following function will handle the conversation with the user
    :return: None
    """
    quitting = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
        server_address = ('', LISTENING_PORT)
        listening_socket.bind(server_address)
        listening_socket.listen(1)
        client_soc, client_address = listening_socket.accept()
        client_soc.sendall("Welcome To The Pink Floyd Database!".encode())
        while not quitting:
            server_msg = client_soc.recv(1024)
            msg = server_msg.decode()
            if "additional_data" in msg:
                additional_data = msg.split("#additional_data:{")[1][:-1]
            
            msg_code = int(msg.split("{")[1][:2])
            if msg_code == 10:
                client_soc.sendall(data.albums_list().encode())
            
            elif msg_code == 20:
                answer = data.album_songs_list(additional_data)
                # print(answer)
                client_soc.sendall(answer.encode())
            
            elif msg_code == 30 or msg_code == 40:
                answer = data.song_data(additional_data)
                client_soc.sendall(answer.encode())

            elif msg_code == 50:
                client_soc.sendall(data.search_for_album(additional_data).encode())

            elif msg_code == 60:
                client_soc.sendall(data.songs_with_word(additional_data).encode())

            elif msg_code == 70:
                client_soc.sendall(data.lyrics_with_word(additional_data).encode())

            elif msg_code == 80:
                quitting = True
                client_soc.sendall("Thank you for using our system!".encode())
            else:
                client_soc.sendall("Invalid input".encode())


def main():
    conversation()


if __name__ == "__main__":
    main()
