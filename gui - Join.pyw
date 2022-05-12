import os
#check if were running on linux
if os.name != "nt":
    exit()

import time
from tkinter import *
from tkinter import messagebox
import socket
import threading
import json

##Attempt to read the config
try:
    with open("config.json", "r") as f:
        config = json.load(f)

except FileNotFoundError:
    messagebox.showerror("Error", "Could not find config.json Please make sure it is in the same directory as this file.")
    exit()  
except Exception as e:
    messagebox.showerror("Error", f"Could not read config.json. reason: {e}")

#####Variables#####
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = config["host"]
PORT = int(config["port"])
FORMAT = config["format"]
USERNAME = config["username"]
HOST_USERNAME = ""

#to properly close the program
def on_closing():
    global sock
    try:
        sock.close()
    except:
        pass
    
    exit()


#try and connect to the server
def connect_to_server():
    global HOST_USERNAME

    try:
        #connect to the server and send our username
        sock.connect((HOST, PORT))
        sock.send(USERNAME.encode(FORMAT))

        #recieve the username of the host
        HOST_USERNAME = sock.recv(1024).decode(FORMAT)

        #say that we are connected
        list_box.insert(END, f"Connected to {HOST_USERNAME}")
        list_box.insert(END, "") #new line

        #start the thread to recieve messages
        threading.Thread(target=receive_message).start()

    except socket.error as e:
        #if we cant connect, say so
        messagebox.showerror("Connection error", f"Could not connect to server. reason: {e}")
        exit()


def send_message():
    try:
        #get message
        message = entry_field.get()
        entry_field.delete(0, END)

        #send the message
        sock.send(message.encode(FORMAT))

        now = time.strftime("%H:%M:%S")
        list_box.insert(END, f"[{now}] {USERNAME}(you): {message}")

    except socket.error as e:
        list_box.insert(END, f"{e}")
        send_button.config(state=DISABLED)
        return

def receive_message():
    print("Now receiving messages...")
    try:
        while True:
            data = sock.recv(1024).decode(FORMAT)
            now = time.strftime("%H:%M:%S")

            if data == "":
                continue
            else:
                list_box.insert(END, f"[{now}] {HOST_USERNAME}: {data}")

    except Exception as e:
        list_box.insert(END, f"{e}")
        send_button.config(state=DISABLED)
        return

#####main gui####
tk = Tk()
tk.title("JOIN")
tk.resizable(False,False)
tk.geometry("500x500")
tk.protocol("WM_DELETE_WINDOW", on_closing)

#where the messages will be displayed
list_box = Listbox(tk)
list_box.place(x=0, y=0, width=500, height=400)

#where the user will enter their message
entry_field = Entry(tk)
entry_field.place(x=0, y=400, width=450, height=25)

#send button
send_button = Button(tk, text="Send", command=send_message)
send_button.place(x=450, y=400, width=50, height=25)

connect_to_server()
tk.mainloop()
