import socket 
import threading
import time
from tkinter import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999
FORMAT = 'utf-8'
username = socket.gethostname()

##Code to properly close the program
def on_closing():
    global sock
    try:
        sock.close()
    except:
        pass

    exit()


def create_server():
    global conn, addr, CONNECTED_USERNAME

    #Saying that were creating the server
    now = time.strftime("%H:%M:%S")
    list_box.insert(END, f"[{now}]Creating server...")

    #try to create the server
    try:
        s.bind((HOST, PORT))
        s.listen(5)
    except socket.error as e:
        list_box.insert(END, f"{e}")
        return

    #if the server is created, then announce it, and wait for a connection
    now = time.strftime("%H:%M:%S")
    list_box.insert(END, f"[{now}]Server created at {HOST}:{PORT}, Waiting for connection...")

    #When a connection is made, accept it and recieve the username (first message)
    conn, addr = s.accept()
    CONNECTED_USERNAME  = conn.recv(1024).decode(FORMAT)

    #send our username
    conn.send(username.encode(FORMAT))

    #say that we are connected
    now = time.strftime("%H:%M:%S")
    list_box.insert(END, f"[{now}]{CONNECTED_USERNAME} Has Connected!")
    list_box.insert(END, "")

    #start the thread to recieve messages
    threading.Thread(target=receive_message).start()

    #setthe button state to allow to send messages
    send_button.config(state=NORMAL)

    

def send_message():
    message = message_entry.get()
    message_entry.delete(0, END)

    if message == "":
        return

    now = time.strftime("%H:%M:%S")
    list_box.insert(END, f"[{now}]{username}(you): {message}")

    conn.send(message.encode(FORMAT))

    pass

def receive_message():
    global conn
    try:
        print("Now receiving messages...")
        
        while True:
            data = conn.recv(1024).decode(FORMAT)
            now = time.strftime("%H:%M:%S")

            list_box.insert(END, f"[{now}]{CONNECTED_USERNAME}: {data}")

    except socket.error as e:
        list_box.insert(END, f"{e}")
        send_button.config(state=DISABLED)
        return
    pass

tk = Tk()
tk.title("Host")
tk.geometry("500x500")
tk.resizable(False, False)
tk.protocol("WM_DELETE_WINDOW", on_closing)

list_box = Listbox(tk)
list_box.place(x=0, y=0, width=500, height=400)

message_entry = Entry(tk)
message_entry.place(x=0, y=400, width=450, height=25)

send_button = Button(tk, text="Send", command=send_message, state=DISABLED)
send_button.place(x=450, y=400, width=50, height=25)

threading.Thread(target=create_server).start()
tk.mainloop()