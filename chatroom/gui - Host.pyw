import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST_USERNAME = "Username"
FORMAT = 'utf-8'
send_history = []

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

#Host server
sock.bind((HOST, PORT))
sock.listen(5)

conn, addr = sock.accept()
print("Connected to:", addr)

conn.send(HOST_USERNAME.encode(FORMAT))

def send_message():
    message = entry_field.get()
    entry_field.delete(0, END)
    conn.send(message.encode(FORMAT))
    send_history.append("\n" + message)
    pass

def receive_message():
    now = time.strftime("%H:%M:%S")
    data = conn.recv(1024).decode(FORMAT)
    message_list.insert(END, f"[{now}] {HOST_USERNAME}: {data}")
    pass

##main gui
tk = Tk()
tk.title("HOST")
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

tk.mainloop()