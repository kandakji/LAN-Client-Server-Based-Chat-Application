import sqlite3
import hashlib

dbconn = sqlite3.connect("chat_users.db")
dbcurs = dbconn.cursor()

'''dbcurs.execute("""create table users(
ID integer primary key autoincrement,
Username char(10) unique,
Password char(30)
);""")
'''

#dbcurs.execute("""INSERT INTO users (Username, Password) VALUES ('Admin','""" + hashlib.sha512(b'chatadmin').hexdigest() + """')""")
#dbcurs.execute("""INSERT INTO users (Username, Password) VALUES ('Admin_sec','""" + hashlib.sha512(b'secchatadmin').hexdigest() + """')""")


dbcurs.execute("""select * from users""")

result = dbcurs.fetchall()

print(result)


#dbcurs.execute("select Password from users where Username = '" + 'Admin' + "'")

#result = dbcurs.fetchall()
#print(result[0][0])


#dbcurs.execute("delete from users")

dbconn.commit()
dbconn.close()