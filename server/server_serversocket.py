import socketserver
import sys
import os
import threading
import socket

BUFFER_SIZE = 1024

def get_file_path_and_size(filename):
        dataset_dir_path = os.path.join(os.getcwd(), 'dataset')
        # cwd: current working directory, concat ke folder dataset
        file_path = os.path.join(dataset_dir_path, filename)
        # path ke file
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

class MyTCPHandler(socketserver.BaseRequestHandler):
   
    def handle(self):
        cur_thread = threading.current_thread()
        while True:
            self.data = self.request.recv(1024)
            
            if self.data:
                split_data = self.data.decode('utf-8').split()
            
                if len(split_data) > 1:
                    command, filename = split_data[0], ' '.join(split_data[1:])
                    # command : string 'unduh', filename : xxx.txt
                    if command.lower() == 'unduh':
                        file_path, file_size = get_file_path_and_size(filename)
                        self.request.sendall(f'{file_size}'.encode())
                        response = self.request.recv(BUFFER_SIZE).decode('utf-8')
                        # if file exists   
                        if file_path and file_size:
                            header_message = f"file-name: {filename},\nfile-size: {file_size},\n\n\n"
                            header_size = bytes(header_message,'utf-8')
                            self.request.sendall(bytes(str(len(header_size)),'utf-8'))
                            response = self.request.recv(BUFFER_SIZE).decode('utf-8')
                            send_file(self.request, file_path, header_message)
                        else:
                            self.request.sendall(f'{filename} not found'.encode())
                
                    else:
                        self.request.sendall(f'Unduh file dengan mengirimkan command \'unduh <nama file>\''.encode())
                else:
                    self.request.sendall(f'Unduh file dengan mengirimkan command \'unduh <nama file>\''.encode())
        
            else:
                return

          
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 5000
    server = ThreadedTCPServer((HOST, PORT), MyTCPHandler)
    # Create the server, binding to localhost on port 9999
    with server:

        try:
            server.serve_forever()
            # Exit the server thread when the main thread terminates and serve many requests
                   
        # Activate the server; this will keep running until you interrupt the program with Ctrl-C
        except KeyboardInterrupt:
            print('closing socket')                    
            server.shutdown()
    