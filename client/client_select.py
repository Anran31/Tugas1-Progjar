import socket
import sys


BUFFER_SIZE = 1024

def download_file(socket ,filename, file_size, header_size):
    with open(filename, 'wb') as file:
        total = 0
        header = True
        while True:
            bytes_read = socket.recv(BUFFER_SIZE)
            total += len(bytes_read)
            if header:
                file.write(bytes_read[header_size:])
                header = False
            else:
                file.write(bytes_read)
            if (file_size + header_size) == total:
                print(f'Finished receiving {filename}')
                break
        file.close()


def connect(client_socket):
    print('>> ',end='', flush=True)
    try:
        while True:
            message = sys.stdin.readline()
            split_message = message.strip().split()

            client_socket.send(bytes(message, 'utf-8'))

            if split_message[0].lower() == 'unduh':
                file_size = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                client_socket.send(bytes('file size received','utf-8'))

                if file_size != '0':
                    header_size = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                    client_socket.send(bytes('header size received','utf-8'))
                    download_file(client_socket, ' '.join(split_message[1:]), int(file_size), int(header_size))
                else:
                    received_data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                    print(received_data)
            else:
                received_data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                print(received_data)

            print('>> ', end='', flush=True)

    except KeyboardInterrupt:
        client_socket.close()
        sys.exit(0)

if __name__ == '__main__':
    server_address = ('127.0.0.1', 5000)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    connect(client_socket)