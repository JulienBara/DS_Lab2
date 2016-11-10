import socket
import sys
from thread import *

if len(sys.argv) > 3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
    nbrCoAllowed = int(sys.argv[3])
else:
    host = "localhost"
    port = 9000
    nbrCoAllowed = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("socket created")

# Bind socket to local host and port
try:
    s.bind((host, port))
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print ('Socket bind complete')

# Start listening on socket
s.listen(1)
print ('Socket now listening')

global serverOn
serverOn = True

global nbrCoClient
nbrCoClient = 0


# Function for handling connections. This will be used to create threads
def clientThread(conn):
    nbrCoClient += 1

    global serverOn
    while serverOn:
        data = conn.recv(4096)

        if not data:
            break

        if data == "KILL_SERVICE\n":
            serverOn = False

        if data[:4] == "HELO":
            text = data[5:]
            conn.send("HELO " + text + "IP:" + host + "\nPort:" + str(port) + "\nStudentID:" + "16337089" + "\n")

    nbrCoClient -= 1
    conn.close()


while serverOn:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))

    if not serverOn:
        break

    if nbrCoAllowed < nbrCoClient:
        print ("To many connected clients")
        conn.close()

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientThread, (conn,))

s.close()
