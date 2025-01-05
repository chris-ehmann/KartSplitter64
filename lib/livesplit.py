import socket
from datetime import datetime, timedelta

SERVER_PORT = 16834
HOST_NAME = 'localhost'

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            s.connect((HOST_NAME, SERVER_PORT))
            break
        except:
            print("Unable to connect to LiveSplit Server. Please ensure that the TCP Server has been started.")

    print("Connected to LiveSplit Server")
    return s

def setup_timer(socket):
    socket.send(b"switchto gametime\n")

def start_run(socket):
    socket.send(b"starttimer\n")
    socket.send(b"setgametime 00:00:03\n")
    socket.send(b"unpausegametime\n")

def reset_run(socket):
    socket.send(b"reset\n")

def split(socket):
    socket.send(b"split\n")

def get_current_split(socket):
    socket.send(b"getsplitindex\n")
    data = int(socket.recv(4096).decode('utf-8'))
    return data

def retroactive_split(socket):
    socket.send(b"getcurrentgametime\n")
    data = socket.recv(4096).decode('utf-8')
    x = data.split("\n")
    datetime_object = datetime.strptime(x[0][:-1], '%H:%M:%S.%f')
    change_time = (datetime_object - timedelta(seconds=2.7)).strftime('%H:%M:%S.%f')
    original_time = datetime_object.strftime('%H:%M:%S.%f')

    socket.send(b"setgametime " + str.encode(change_time) + b"\n")
    socket.send(b"split\n")
    socket.send(b"setgametime " + str.encode(original_time) + b"\n")