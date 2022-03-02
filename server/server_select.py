import socket
import select
import sys
import os

BUFFER_SIZE = 1024

def connect(server_socket, input_socket):
    try:
        while True:
            read_ready, write_ready, exception = select.select(input_socket, [], [])
            
            for sock in read_ready:
                if sock == server_socket:
                    client_socket, client_address = server_socket.accept()
                    input_socket.append(client_socket)        
                
                else:            	
                    # data = sock.recv(1024).decode('utf-8')
                    data = sock.recv(1024)
                    # print(data.decode('utf-8'))
                    if data:
                        print(data)
                        split_data = data.decode('utf-8').split()
                        if len(split_data) > 1:
                            command, filename = split_data[0], ' '.join(split_data[1:])
                            print(command, filename)
                            if command.lower() == 'unduh':
                                filepath = get_file_path(filename)
                                if filepath:
                                    print('sending data in split_data')
                                    # sock.sendall(f'{filename} found'.encode())
                                    send_file(input_socket, sock, filepath)
                                else:
                                    print('sending data in split_data')
                                    sock.sendall(f'{filename} not found'.encode())
                            else:
                                print('sending data in split_data')
                                sock.sendall(f'Unduh file dengan mengirimkan command \'unduh <nama file>\''.encode())
                        else:
                            print('sending data in split_data')
                            sock.sendall(f'Unduh file dengan mengirimkan command \'unduh <nama file>\''.encode())
                    
                    # elif data == b'\n':
                    #     print('sending data in elif data', data.decode('utf-8'))
                    #     # sock.sendall(data.encode())
                    #     sock.sendall(f'Unduh file dengan mengirimkan command \'unduh <nama file>\''.encode())
                    #     # sock.send(data)

                    else:
                        print('closing socket')                    
                        sock.close()
                        input_socket.remove(sock)

    except KeyboardInterrupt:        
        server_socket.close()
        sys.exit(0)

def get_file_path(filename):
    dataset_dir_path = os.path.join(os.getcwd(), 'dataset')
    print(dataset_dir_path)

    file_path = os.path.join(dataset_dir_path, filename)
    print(file_path)

    if os.path.exists(file_path):
        return file_path
    return ''

def send_file(input_socket, socket, filepath):
    with open(filepath, 'rb') as file:
        while True:
            # read the bytes from the file
            bytes_read = file.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                print('end of file')
                socket.sendall(bytes('EOF','utf-8'))
                break
            socket.sendall(bytes_read)
            # we use sendall to assure transimission in 
            # busy networks
        file.close()


if __name__ == "__main__":
    server_address = ('172.20.28.238', 5000)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(5)

    input_socket = [server_socket]
    connect(server_socket, input_socket)