import serial
import sqlite3
import time
import datetime

# connexion a la bdd et au port série
ser = serial.Serial("COM35", 9600)


# fonction d'écoute sur le port série

def serial_listener():
    if ser.isOpen():
        print(f'Port {ser.name} open')
        while True:
            line = ser.readline()
            # rstrip to avoid end of line problem
            print(line.decode().rstrip())
            if len(line.decode().rstrip()) == 8:
                bdd(line.decode().rstrip())


# fonction d'écriture sur la liaison série

def serial_writer(message):
    ser.write(message)


# fonction de select du nombre de trajets de l'utilisateur

def bdd(uid):
    conn = sqlite3.connect('matcha.db')
    c = conn.cursor()
    now = datetime.datetime.now()
    date = str(now.day) + '/' + str(now.month) + '/' + str(now.year) + ' ' + str(now.hour) + ':' +  str(now.minute)
    c.execute("SELECT * FROM users WHERE uid = ?", (uid,))
    result = c.fetchall()
    tickets = result[0][2] - 1
    c.execute("SELECT bip_card_time FROM users WHERE uid = ?",(uid,))
    date_from_user = c.fetchall()
    if date != date_from_user[0][0]:
        c.execute("UPDATE users SET bip_card_time = ? WHERE uid = ?", (date, uid))
        if tickets <= -1:
            c.execute("UPDATE users SET tickets = 0 WHERE uid = ?", (uid,))
            tickets = -1
        else:
            c.execute("UPDATE users SET tickets = ? WHERE uid = ?", (tickets, uid))
        serial_writer(str(tickets).encode("ascii"))
        print(tickets)
        c.fetchall()
        conn.commit()
    else:
        serial_writer('dv'.encode('ascii'))
    conn.close()

serial_listener()
