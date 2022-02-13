# Reverse-Shell
## Note that this has only been tested on a Windows machine, if you expiriense any bugs with Mac or Linux, post an issue and I will try to fix it.

## Also any Mac or Linux users, you can add steps for your operating system by posting instruction in the issues tab and I will itegrate them with the official instructions.

A Reverse Shell puilt in Python

# Before Downloading
This tutorial assumes you already have python installed on your machine

Make sure you have all the modules needed, modules include:

### socket, psutil, colorama

If you don't have these, run the command below:
```
pip install socket psutil colorama
```

# Downloading

## 1).================================================
Run the command Below:
```
git clone https://github.com/lamaprogramer/Reverse-Shell
```

You will need to do this on the machine you want the server to be on, as well as the machine you want the client to be on.

This will clone the repository into your cwd(current working directory).

## 2).================================================
Afterward, the folder system should look like this
```
Reverse-Shell
      |
      |--client_folder
      |         |--client.py
      |         |--start_clent.bat
      |
      |--server_folder
      |         |--server.py
      |         |--start_server.bat
```
Inside the **Reverse-Shell** folder, you should see two folders: **client_folder** and **server_folder**.

Move the **server_folder** to a place of your liking( *or leave it where it is as location doesn't matter* ).

Then, on a different machine, move the **client_folder** to a place of your liking( *or leave it where it is as location doesn't matter* ).

## 3).================================================
Now on your main machine, you need to open **server.py** in the **server_folder**.

After opening the file, you must add the ip of your remote machine into the **WHITELIST_IPS** variable, found on line 11
```python
line 10:   SERVER_HOST = "0.0.0.0"
line 11:   WHITELIST_IPS = [""] # Add your remote ip inside the double-quotes
line 12:   SERVER_PORT = 5003
line 13:   BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
line 14:   SEPARATOR = "<sep>"
```

This will allow your remote machine to connect to the server(this is purely for security reasons)



Then, on your remote machine, you need to go into **client.py** in the **client_folder**.

After opening the file, you must then specify the ip of your machine with the server

You can find the ip by running:
```
ipconfig
```
on your main machine

## 4).================================================
Run the Batch files in each folder, this will start up each end

Make sure you run the server end first, or else the client wont be able to connect

## 5).================================================
If everything ran correctly, After you boot up the server, you should see:
```
Listening as 0.0.0.0:5003 ...
```
And after the client connects, you should something similar to this:
```
REMOTEIP:REMOTEPORT Connected!
[+] Current working directory: C:\Users\remotepc\OneDrive\Desktop\Reverse Shell\client_folder
C:\Users\remotepc\OneDrive\Desktop\Reverse Shell\client_folder $>
```

## 6).================================================
By this point, you should have nearly full control of the remote pc, you can run any command, as well as transfer files using custom commands built into the Reverse Shell


# Features
## Custom Commands
1). upload: uploads files to the client machine

2). download: downloads files from the client machine

3). sysinf: get the system info of the client machine

4). msg: sends a message to the client machine's terminal, the client then has the choise to respond

5). help: displays a list of all custom commands, and a basic description of them

6). exit: shuts down the socket

## Built-in whitelist
A whitelist was built into the Reverse Shell to make sure that only the people you want to join can join



# ToDo
1). Add json configs for configuring ips

2). Add Multithreading

3). Add a hjack command to control keyboard and mouse input

