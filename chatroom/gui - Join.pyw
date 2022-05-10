import os
#check if were running on linux
if os.name != "nt":
    exit()

import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import socket
import threading

#####Variables#####
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "192.168.56.1"
PORT = 9999
FORMAT = 'utf-8'

ran = False
send_history = []

#try and connect to the server
try:
    sock.connect((HOST, PORT))
except socket.error as e:
    messagebox.showerror("Connection error", "Could not connect to server.")
    exit()

#HOST_USERNAME = sock.recv(1024).decode(FORMAT) #The first message recieved from the server is the username
HOST_USERNAME = "Server"

##################

def send_message():
    message = entry_field.get()
    entry_field.delete(0, END)
    sock.send(message.encode(FORMAT))
    send_history.append("\n" + message)
    pass

def receive_message():
    print("Now receiving messages...")
    while True:
        now = time.strftime("%H:%M:%S")
        data = sock.recv(1024).decode(FORMAT)
        print(f"{now} {HOST_USERNAME}: {data}")
        message_list.insert(END, f"[{now}] {HOST_USERNAME}: {data}")
        pass

tk = Tk()
tk.withdraw()
######Connect to server GUI######
connect_tk = tk.toplevel()
connect_tk.title("Connect to server")
connect_tk.geometry("300x100")
connect_tk.resizable(False, False)


connect_tk.mainloop()


#####main gui####
tk.deiconify()
tk.title("JOIN")
tk.resizable(False,False)
tk.geometry("500x500")

#where the messages will be displayed
message_list = Listbox(tk)
message_list.place(x=0, y=0, width=500, height=400)

#where the user will enter their message
entry_field = Entry(tk)
entry_field.place(x=0, y=400, width=450, height=25)

#send button
send_button = Button(tk, text="Send", command=send_message)
send_button.place(x=450, y=400, width=50, height=25)

#start receiving messages
threading.Thread(target=receive_message).start()

tk.mainloop()