import socket
import sys


if len(sys.argv) > 3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
    nbrCoAllowed = int(sys.argv[3])
else:
    host = "localhost"
    port = 8000
    nbrCoAllowed = 10


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("socket created")

#Bind socket to local host and port
try:
    s.bind((host, port))
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print ('Socket bind complete')

#Start listening on socket
s.listen(nbrCoAllowed)
print ('Socket now listening')

 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print ('Connected with ' + addr[0] + ':' + str(addr[1]))
     
s.close()