import socket
import pickle
import uuid
from datetime import datetime

now = datetime.now()
now_string = now.strftime("%d/%m/%Y %H:%M:%S")

HEADER = 1024
PORT = 8000
SECOND_PORT = 8001
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
SECOND_ADDR = (SERVER, SECOND_PORT)

unique_id = str(uuid.uuid4())
code_received = None
final_message = None

class Client:
    def __init__(self, ADDR):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.port = ADDR[1]

    def send(self, msg):
        global code_received
        global final_message

        message = pickle.dumps(msg)
        self.client.send(message)
        msg_received = pickle.loads(self.client.recv(HEADER))
        print(msg_received)
        code_received = msg_received
        if not final_message:
            self.generate_message(code_received)
        


    def generate_message(self, code_received):
        global final_message
        global unique_id
        final_message = [f"Unique code received on {now_string}", unique_id, code_received]



client = Client(ADDR)

client.send(unique_id)

client.send(DISCONNECT_MESSAGE)

second_client = Client(SECOND_ADDR)

second_client.send(final_message)

second_client.send(DISCONNECT_MESSAGE)
