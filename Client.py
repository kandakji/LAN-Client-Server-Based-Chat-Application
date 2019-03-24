#Client Code
import socket
import threading
import getpass


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    users = []

    def sendMsg(self):
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))

    def __init__(self):
        try:
            self.sock.connect(("192.168.0.107",10000))
            while True:
                username = input("username:")

                self.sock.send(bytes("username:_-_" + username, 'utf-8'))

                data = self.sock.recv(1024)

                data = str(data,'utf-8')

                if data == "verifieduser":
                    print("verified")

                    password = getpass.getpass(prompt='Password: ', stream=None)

                    self.sock.send(bytes("password:_-_" + password, 'utf-8'))

                    data = self.sock.recv(1024)

                    data = str(data, 'utf-8')

                    if data == "authenticated":
                        print("authenticated")
                        print("--------------------------------------")
                        break


                    elif data == "notauthenticated":
                        print("Username and Password are not valid.")
                        continue

                elif data == "notverified":
                    print("not verified")
                    continue


            iThread = threading.Thread(target=self.sendMsg)
            iThread.daemon = True
            iThread.start()

            while True:
                data = self.sock.recv(1024)
                if not data:
                    break
                print(str(data, 'utf-8'))

        except:
            print("Server is currently unavailable.")



client=Client()








