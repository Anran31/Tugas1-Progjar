import socket
import sys


BUFFER_SIZE = 1024

def download_file(socket ,filename):
    with open(filename, 'wb') as file:
        counter = 0
        while True:
            # read 1024 bytes from the socket (receive)
            print('receiving.....', counter)
            counter += 1
            bytes_read = socket.recv(BUFFER_SIZE)
            if bytes_read == bytes('EOF','utf-8'):
                # nothing is received
                # file transmitting is done
                print('break')
                break
            file.write(bytes_read)
        # write to the file the bytes we just received
        file.close()

server_address = ('172.20.28.238', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# sys.stdout.write('>> ')
print('>> ',end='')
with open('apa.txt', 'wb') as file:
    file.write(b'tes')
    file.close()

try:
    while True:
        message = sys.stdin.readline()
        split_message = message.strip().split()
        print(message)
        # message = input('>> ')
        client_socket.send(bytes(message, 'utf-8'))
        # client_socket.send(message.encode())
        if split_message[0].lower() == 'unduh':
            download_file(client_socket, ' '.join(split_message[1:]))
        else:
            received_data = client_socket.recv(1024).decode('utf-8')
        # sys.stdout.write(received_data)
        # print(received_data)
        print('>> ', end='')
        # sys.stdout.write('>> ')

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)