# Reverse-Shell
A Reverse Shell puilt in Python

# Downloading

The easiest way to get the Reverse Shell is by using the "git" command.

### 1).=======================================================================
Run the command Below:
```
git clone https://github.com/lamaprogramer/Reverse-Shell
```
You will need to do this on the machine you want the server to be on, and the machine you want the client to be on.

This will clone the repository into your cwd(current working directory).

### 2).=======================================================================
Make sure you have all of the modules needed to run the code

### 3).=======================================================================
inside the repository folder, you should see two folders: **client_folder** and **server_folder**.
Move the server_folder to a place of your liking.
Then, on a different machine, move the client folder to a place of your liking.

### 4).=======================================================================
Now on your main machine, you need to open **server.py** in the **server_folder**.

After opening the file, you must add the ip of your remote machine into the **WHITELIST_IPS** variable, found on line 11

This will allow your remote machine to connect to the server(this is purely for security reasons)



Then, on your remote machine, you need to go into **client.py** in the **client_folder**.

After opening the file, you must then specify the ip of your machine with the server

You can find the ip by running:
```
ipconfig
```
on your main machine

### 4).=======================================================================
Run the Batch files in each folder, this will start up each end
Make sure you run the server end first, or else the client wont be able to connect

### 5).=======================================================================
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

### 6).=======================================================================
By this point, you should have nearly full control of the remote pc, you can run any command, as well as transfer files using custom commands built into the Reverse Shell
