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
s.listen(nbrCoAllowed)
print ('Socket now listening')


# Function for handling connections. This will be used to create threads
def clientThread(conn):
    # Sending message to connected client
    # conn.send('Welcome to the server. Type something and hit enter\n')  # send only takes string

    # infinite loop so that function do not terminate and thread do not end.
    while True:

        # #Receiving from client
        # data = conn.recv(1024)
        # reply = 'OK...' + data
        # if not data: 
        #     break

        # conn.sendall(reply)

        data = conn.recv(4096)

        if not data:
            break

        if data == "KILL_SERVICE\n":
            conn.send("Not implemented yet")

        if data == "HELO text\n":
            conn.send("HELO text\nIP:[ip address]\nPort:[port number]\nStudentID:[your student ID]\n")

    # came out of loop
    conn.close()


# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientThread, (conn,))

s.close()
