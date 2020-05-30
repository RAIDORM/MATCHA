from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import users, Base
from os import path
import secrets
import hashlib

app = Flask(__name__)

app.secret_key = "RtvVBW5zju2MPBlEFAac2BsclpzMxCWr"


engine = create_engine(
    'sqlite:///R:\\MATCHA-master\\database.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        data['uid'] = data['uid'].upper()
        user_exist = session.query(users).filter(users.uid == data['uid']).scalar()
        if user_exist == None:
            if len(data['uid']) == 8:
                user = users(name=data['prenom'] + " " + data['nom'], password=password(data['password']), uid=data['uid'], tickets=0)
                session.add(user)
                session.commit()
                return jsonify({
                    'title': 'Inscription réussite !',
                    'body': "Bonjour " + data['prenom'] + " heureux de vous avoir parmi nous !"
                })
            else:
                return jsonify({
                    'error': "Désolé mais l'UID doit faire 8 caractères."
                })
        else:
            return jsonify({
                'error': "Désolé mais cet UID est déjà utilisé merci de vous connecter."
            })



@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        data['uid'] = data['uid'].upper()
        user_info = session.query(users).filter(users.uid == data['uid']).first()
        if user_info != None:
            if password(data['password']) == user_info.password:
                return jsonify({
                    'name': user_info.name,
                    'tickets': user_info.tickets,
                    'uid': user_info.uid,
                    'pass': user_info.password
                })
            else:
                return jsonify({
                    'error': "Désolé mais le mot de passe ne correspond pas !"
                })
        else:
            print('user false')
            return jsonify({
                'error': "Désolé mais je ne connais pas cet utilisateur !"
            })


@app.route('/paiement', methods=['POST'])
def paiement():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        user_info = session.query(users).filter(users.uid == data['uid_paiement']).first()
        if user_info!= None:
            if data['password_paiement'] == user_info.password:
                new_tickets = user_info.tickets + int(data['tickets_paiement'])
                user_info.tickets = new_tickets
                session.commit()
                return jsonify({
                    'title': "Achat effectué",
                    'body' : 'Votre achat pour ' + data['tickets_paiement'] + ' tickets à été effectué',
                    'tickets' : new_tickets
                })
            else:
                return jsonify({
                    'error': "Désolé mais le mot de passe ne correspond pas !",
                    })
        else:
            return jsonify({
                'error': "Désolé mais je ne connais pas cet utilisateur !",
                })


#INPUT : password | type : STR
#FUNCTION : hash password
#RETURN : hashed password sha-256 | Type : String
def password(password):
    if not path.exists('secret_token.txt'):
        f= open("secret_token.txt","w+")
        f.write(secrets.token_hex(15))
        f.close()
    f = open("secret_token.txt", "r")
    password = password[::-1] + f.read()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash

if __name__ == '__main__':
    app.run(host='0.0.0.0')
