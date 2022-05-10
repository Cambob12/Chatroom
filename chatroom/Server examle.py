import socket
import threading
import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
sock.bind((IP, PORT))
sock.listen(1)

print(f"[LISTENING] Server is listening on {IP}:{PORT}")

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr[0]}:{addr[1]} connected.")
    
    # send message to client saying "Connected"    
    server_info = f"Connected to: {IP}:{PORT}".encode()
    conn.send(server_info)

    try:
        while True:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            
            # receive data from client
            data = conn.recv(1024).decode()
            data = str(data)

            #show the data
            print(f"[{addr[0]}:{addr[1]}][{now}] {data}")

            #########################COMMANDS#############################            
            if data == " ":
                continue

            elif data == "/quit":
                print(f"[{addr[0]}:{addr[1]}][{now}] Disconnected. (Disconnected by client)")
                break

            elif data == "/time":
                conn.send(f"\nServer time: {now}".encode())
            
            elif data == "/help":
                conn.send("\n/quit - to quit\n/time - to get the time\n/help - to get this message".encode())

            else:
                conn.send(b"received")
                pass

            
            ###############################################################



            # send data back to client
            
    
        conn.close()

    except Exception as e:
        #Error handling
        #sock.send("force_disconnect".encode())
        print(f"[{addr[0]}:{addr[1]}][{now}] Disconnected by server, Reason: {e}")
        conn.close()


while True:
    conn, addr = sock.accept()

    # create a thread to handle the client
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")