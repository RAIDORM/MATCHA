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
    c.execute('SELECT name, tickets, bip_card_time, uid FROM users ORDER BY tickets ASC')
    data = c.fetchall()
    c.execute('SELECT date FROM passages')
    passages = c.fetchall()
    a, b, c, d, e, f= (0,)*6
    for user in data:
        tickets = user[1]
        if tickets >= 40:
            a += 1
        if tickets >= 30:
            b += 1
        if tickets >= 20:
            c += 1
        if tickets >= 10:
            d += 1
        if tickets >= 5:
            e += 1
        if tickets < 5:
            f += 1
    graph = [a, b, c, d, e, f]
    conn.close()
    return render_template("admin.html", data=data, graph=graph)


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
