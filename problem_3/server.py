import socket
import threading
import pickle
import uuid
import select


HEADER = 1024
SERVER = socket.gethostbyname(socket.gethostname())
DISCONNECT_MESSAGE = "DISCONNECT"
PORTS = [8000, 8001]

id_storage = {}

def create_socket(TCP_PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, TCP_PORT))
    print(f"Server is listening on {SERVER}")
    server.listen()

    return server

def main():

    read_list = []

    for TCP_PORT in PORTS:
        read_list.append(create_socket(TCP_PORT))

    while True:
        #print(read_list)
        readable, writable, exceptional = select.select(read_list, [], read_list)
        for s in readable:
            print("client connected")
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"{int(threading.activeCount()) - 1} active connections")

def handle_client(conn, addr):
    print(f"{addr} connected to the server")
    print(conn.getsockname()[1])
    connected = True
    while connected:
        try:
            received_msg = conn.recv(HEADER)
            msg = pickle.loads(received_msg)
            if conn.getsockname()[1] == 8000:
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"{addr} sent {msg}")
                    new_msg = pickle.dumps(msg)
                    conn.send(new_msg)
                else:
                    id_received(msg)
                    reply = id_storage[msg]
                    print(f"{addr} sent {msg}")
                    new_message = pickle.dumps(reply)
                    conn.send(new_message)
            else:
                complete_data_received(msg)
                new_msg = pickle.dumps("[COMPLETE] Data saved to log.")
                conn.send(new_msg)
        except EOFError:
            pass

    conn.close()

def id_received(msg):
    global id_storage
    if msg in id_storage:

        print("[ERROR] ID already exist")
    elif msg == DISCONNECT_MESSAGE:
        pass
    else:
        unique_code = str(uuid.uuid4())
        id_storage.update({msg: unique_code})

def complete_data_received(msg):
    global id_storage
    if msg[1] in id_storage:
        if id_storage[msg[1]] == msg[-1]:
            with open("Server_log.txt", "a+") as log:
                log.write(f"{msg[0]}")
                log.write("\n")

        else:
            error = "[ERROR] data provided does not match server's data"
            new_msg = pickle.dumps(error)
            conn.send(new_msg)


if __name__ == "__main__":
    main()
