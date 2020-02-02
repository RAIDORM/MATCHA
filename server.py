from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def users():
    if len(request.form.to_dict()) != 0:
        result = request.form.to_dict()
        conn = sqlite3.connect('matcha.db')
        c = conn.cursor()
        c.execute('SELECT name, tickets, bip_card_time, uid FROM users WHERE name LIKE ?',
                  ('%' + result['name'] + '%',))
        data = c.fetchall()
        conn.close()
        return render_template('index.html', data=data)
    else:
        return render_template('index.html')


@app.route('/payment', methods=['GET'])
def payment():
    result = request.args.get('user')
    conn = sqlite3.connect('matcha.db')
    c = conn.cursor()
    c.execute('SELECT name, tickets, uid FROM users WHERE name = ?', (result,))
    data = c.fetchall()
    conn.close()
    return render_template('user.html', data=data)


@app.route('/admin')
def admin():
    conn = sqlite3.connect('matcha.db')
    c = conn.cursor()
    c.execute('SELECT name, tickets, bip_card_time, uid FROM users')
    users = c.fetchall()
    conn.close()
    return render_template("admin.html", users=users)


@app.route('/result', methods=['POST'])
def result():
    conn = sqlite3.connect('matcha.db')
    c = conn.cursor()
    result = request.form.to_dict()
    trajet = int(result['nb_trajet']) + int(result['trajet_actuel'])
    c.execute('UPDATE users SET tickets = ? WHERE uid = ?', (trajet, result['uid']))
    conn.commit()
    conn.close()
    return render_template('success.html', trajet=result['nb_trajet'])


if __name__ == '__main__':
    app.run()
