import serial
import datetime
from serial.tools import list_ports

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import de sqlalchemy et de ma table users
from database_setup import users, Base

# connexion a la bdd
engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
# creation d'une session de connexion a la bdd
DBSession = sessionmaker(bind=engine)
session = DBSession()

# configuration du port série
print('Port COM trouvés sur votre ordinateur :')
print('---------------------------------------')
for port in serial.tools.list_ports.comports():
    x = str(port)
    if 'arduino' in x.lower():
        print(x + ' (Recommandé)')
print('---------------------------------------')
print('Entrez le port COM de votre arduino')
com_number = input()
ser = serial.Serial("COM" + com_number, 9600)


# fonction d'écoute sur le port série

def serial_listener():
    if ser.isOpen():
        print(f'Port {ser.name} open')
        while True:
            line = ser.readline()
            result = line.decode().rstrip()
            # rstrip pour enlever les EOL et 8 pour la lenght de l'UID
            if len(result) == 8:
                bdd(result)
    else:
        print('port closed')
        input("Press any key to continue...")
# fonction d'écriture sur la liaison série

def serial_writer(message):
    ser.write(message)


# fonction de select du nombre de trajets de l'utilisateur

def bdd(uid):
    # récupération de la date
    date = datetime.datetime.now().strftime('%d/%m/%Y/%H:%M')
    # Requête de toute la ligne correspondant à l'uid en paramètre
    user_info = session.query(users).filter(users.uid == uid).one()
    # Si la date actuelle différente de la date dans la bdd
    if date != user_info.bip_card_time:
        # mise a jour de la date dans la bdd
        user_info.bip_card_time = date
        tickets = user_info.tickets
        # Si l'utilisateur a 0 trajet alors on revoit -1 sinon renvoi du nombre de
        # trajets acheté et on remet dans tous les cas le nombre de trajets a 0
        # dans la bdd.
        user_info.tickets = 0
        serial_writer(str(tickets).encode("ascii"))
        print(tickets)
    else:
        # dv pour déjà validé
        serial_writer('dv'.encode('ascii'))
    session.commit()


serial_listener()
