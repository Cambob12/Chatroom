import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "192.168.56.1"
PORT = 9999
FORMAT = 'utf-8'

ran = False
send_history = []

#connect to server
try:
    sock.connect((HOST, PORT))
except socket.error as e:
    print("Connection error: %s")

#HOST_USERNAME = sock.recv(1024).decode(FORMAT) #The first message recieved from the server is the username
HOST_USERNAME = "Username"

def send_message():
    message = entry_field.get()
    entry_field.delete(0, END)
    sock.send(message.encode(FORMAT))
    send_history.append("\n" + message)
    pass

def receive_message():
    now = time.strftime("%H:%M:%S")
    data = sock.recv(1024).decode(FORMAT)
    message_list.insert(END, f"[{now}] {HOST_USERNAME}: {data}")
    pass

def run_once():
    global ran
    if ran == False:
        ran = True

        receive_thread = threading.Thread(target=receive_message).start()
        pass
    pass


##main gui
tk = Tk()
tk.title("JOIN")
tk.resizable(False,False)
tk.geometry("500x500")

#where the messages will be displayed
message_list = Listbox(tk, width=30, height=10)
message_list.grid(row=0, column=0, columnspan=2, rowspan=2)

#where the user will enter their message
entry_field = Entry(tk, width=30)
entry_field.grid(row=2, column=0, columnspan=2)

#send button
send_button = Button(tk, text="Send", command=send_message)
send_button.grid(row=2, column=2)

#see history button
Button(tk, text="History", command=lambda: messagebox.showinfo("Title", send_history)).grid(row=3, column=0)
run_once()
tk.mainloop()
