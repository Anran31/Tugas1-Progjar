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
                    data = sock.recv(1024)
                    if data:
                        split_data = data.decode('utf-8').split()
                        if len(split_data) > 1:
                            command, filename = split_data[0], ' '.join(split_data[1:])

                            if command.lower() == 'unduh':
                                file_path, file_size = get_file_path_and_size(filename)
                                sock.sendall(f'{file_size}'.encode())
                                response = sock.recv(BUFFER_SIZE).decode('utf-8')

                                if file_path and file_size:
                                    header_message = f"file-name: {filename},\nfile-size: {file_size},\n\n\n"
                                    header_size = bytes(header_message,'utf-8')
                                    sock.sendall(bytes(str(len(header_size)),'utf-8'))
                                    response = sock.recv(BUFFER_SIZE).decode('utf-8')
                                    send_file(sock, file_path, header_message)
                                else:
                                    sock.sendall(f'{filename} not found'.encode())

                            else:
                                sock.sendall(f'Unduh file dengan mengirimkan command \'unduh <nama file>\''.encode())

                        else:
                            sock.sendall(f'Unduh file dengan mengirimkan command \'unduh <nama file>\''.encode())

                    else:
                        print('closing socket')                    
                        sock.close()
                        input_socket.remove(sock)

    except KeyboardInterrupt:        
        server_socket.close()
        sys.exit(0)

def get_file_path_and_size(filename):
    dataset_dir_path = os.path.join(os.getcwd(), 'dataset')

    file_path = os.path.join(dataset_dir_path, filename)

    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        return file_path, file_size
    return '', 0

def send_file(socket, filepath, header_message):
    temp_file_name = 'temp_' + os.path.basename(filepath)
    with open(temp_file_name, 'wb') as file:
        file.write(bytes(header_message, 'utf-8'))
        with open(filepath, 'rb') as real_file:
            file.write(real_file.read())
            real_file.close()
        file.close()

    with open(temp_file_name, 'rb') as file:
        while True:
            bytes_read = file.read(BUFFER_SIZE)
            if not bytes_read:
                file_name = os.path.basename(filepath)
                print(f'Finished sending {file_name}')
                break
            socket.sendall(bytes_read)
        file.close()
    
    os.remove(temp_file_name)


if __name__ == "__main__":
    server_address = ('127.0.0.1', 5000)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(5)

    input_socket = [server_socket]
    connect(server_socket, input_socket)