import socket
import threading
import sqlite3
import hashlib

class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self):
        
        self.sock.bind(('0.0.0.0',10000))
        self.sock.listen(2)

    def authenticate(self, c):
        while True:
            try:
                data = c.recv(1024)
            except:
                c.close()
                return 0

            if "username:_-_" in str(data, 'utf-8'):
                global username
                username = str(data, 'utf-8').replace('username:_-_', '')

                try:
                    dbconn = sqlite3.connect("chat_users.db")
                    dbcurs = dbconn.cursor()
                    dbcurs.execute("select Username, Password from users where Username = '" + username + "'")
                    result = dbcurs.fetchone()
                    dbconn.commit()
                    dbconn.close()
                except:
                    try:
                        dbcurs.execute("select * from users")
                        dbconn.rollback()
                        dbconn.close()
                        return 0
                    except:
                        return 0

                if str(result) == "None":
                    c.send(bytes("notverified", 'utf-8'))
                    continue
                else:
                    c.send(bytes("verifieduser", 'utf-8'))

                    try:
                        password = c.recv(1024)
                    except:
                        c.close()
                        return 0

                    password = str(password, 'utf-8').replace('password:_-_', '')
                    password = hashlib.sha512(bytes(password, 'utf-8')).hexdigest()

                    if password == result[1]:
                        c.send(bytes("authenticated", 'utf-8'))
                        self.connections.append(c)
                        print(username + " is connected")
                        return 1
                    else:
                        c.send(bytes("notauthenticated", 'utf-8'))
                        continue


    def handler(self, c,a):
        auth = self.authenticate(c)
        if auth == 1:
            while True:
                try:
                    data = c.recv(1024)

                    data = username + " : " + str(data, 'utf-8')

                    for connection in self.connections:
                        if connection != c:
                            connection.send(bytes(data, 'utf-8'))
                except:
                    print(username + " is disconnected")
                    self.connections.remove(c)
                    c.close()
                    break

        else:
            c.close()
            return

    def run(self):
        while True:

            c, a = self.sock.accept()

            cThread = threading.Thread(target=self.handler, args=(c,a))
            cThread.daemon = True
            cThread.start()










server = Server()
server.run()
