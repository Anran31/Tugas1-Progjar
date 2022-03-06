import socket
import sys

HOST, PORT = "127.0.0.1", 5000
# data = " ".join(sys.argv[1:])

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


# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
        # sock.sendall(bytes(data + "\n", "utf-8"))
    # # Receive data from the server and shut down
    # received = str(sock.recv(BUFFER_SIZE), "utf-8")
    # flush : write everything to terminal tanpa menunggu buffer
    print('>> ',end='', flush=True)
    try:
        while True:
            message = sys.stdin.readline() 
            # readline : buat read escape character >>
            split_message = message.strip().split()
            # strip string inputan trus di split per kata
            sock.send(bytes(message, 'utf-8'))

            if split_message[0].lower() == 'unduh':
                file_size = sock.recv(BUFFER_SIZE).decode('utf-8')
                sock.send(bytes('file size received','utf-8'))

                if file_size != '0':
                    header_size = sock.recv(BUFFER_SIZE).decode('utf-8')
                    sock.send(bytes('header size received','utf-8'))
                    download_file(sock, ' '.join(split_message[1:]), int(file_size), int(header_size))
                else:
                    received_data = sock.recv(BUFFER_SIZE).decode('utf-8')
                    print(received_data)
            else:
                received_data = sock.recv(BUFFER_SIZE).decode('utf-8')
                print(received_data)

            print('>> ', end='', flush=True)

    except KeyboardInterrupt:
        sock.close()
        # sys.exit(0)

# print("Sent:     {}".format(data))
# print("Received: {}".format(received))