from flask import Flask, render_template, request, redirect
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect('bankdatabase.db')
c = conn.cursor()

# c.execute('''CREATE TABLE customer1
#                (sno INTEGER,name TEXT,email TEXT,transactionid INTEGER,current REAL)''')
# c.execute('''CREATE TABLE transferhistorys
#                (yourid INTEGER  , othersid INTEGER , amount real)''')
# conn.commit()
# conn.close()

app = Flask(__name__, static_url_path='', static_folder='templates/')


@app.route('/')
def serve_frontend():
    print("Helooooooo ")
    return render_template('index.html')


@app.route('/insertdb/')
def insert():
    conn = sqlite3.connect('bankdatabase.db')
    c = conn.cursor()
    records = [(1, 'Chandler', 'chandler@gmail.com', 101, 500),
               (2, 'Joey', 'joey@gmail.com', 102, 500),
               (3, 'Ranchel', 'ranchel@gmail.com', 103, 500),
               (4, 'Monica', 'monica@gmail.com', 104, 500),
               (5, 'Ross', 'ross@gmail.com', 105, 500),
               (6, 'Phoebe', 'phoebe@gmail.com', 106, 500),
               (7, 'Gunther', 'gunther@gmail.com', 107, 500),
               (8, 'Janice', 'janice@gmail.com', 108, 500),
               (9, 'Mike', 'mike@gmail.com', 109, 500),
               (10, 'Jane', 'jane@gmail.com', 110, 500)]
    c.executemany('INSERT INTO customer1 VALUES (?,?,?,?,?);', records)

    conn.commit()
    conn.close()
    return "SUCCESS"


@app.route('/viewallcust')
def getallcust():
    conn = sqlite3.connect('bankdatabase.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM customer1")
    allcustomer = c.fetchall()
    print(allcustomer)
    conn.commit()
    conn.close()
    return render_template('new_views.html', allcustomer=allcustomer)


@app.route('/view/<int:sno>')
def viewcust(sno):
    conn = sqlite3.connect('bankdatabase.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM customer1 WHERE sno=" + str(sno))
    cust = c.fetchall()
    # print(cust)
    conn.commit()
    conn.close()
    return render_template('view_onecust.html', cust=cust)


@app.route('/inputinfo/<int:sno>', methods=['GET'])
def inputid(sno):
    conn = sqlite3.connect('bankdatabase.db')
    c = conn.cursor()
    c.execute("SELECT transactionid FROM customer1 WHERE sno=" + str(sno))
    data = c.fetchone()
    if data:
        tid = data[0]
    print(tid)
    conn.commit()
    conn.close()
    return render_template('new_transfer.html', tid=tid)


@app.route('/inputinfo/', methods=['POST'])
def inputblock():
    if request.method == 'POST':
        ytid = request.form['ytid']
        tid = request.form['tid']
        amount = request.form['Am']
        # print(amount)
        conn = sqlite3.connect('bankdatabase.db')
        c = conn.cursor()
        c.execute('INSERT INTO transferhistorys VALUES (?,?,?);',
                  (ytid, tid, amount))
        c.execute("SELECT current FROM customer1 WHERE transactionid ="+ytid)
        s1 = c.fetchall()
        # print(s1)
        todo_array = []
        for t in s1:
            todo_array.append(t)
        l = json.dumps(todo_array[0])
        res = int(float(l[1:-2]))
        val = int(res)-int(amount)
        # print(val)
        c.execute("SELECT current FROM customer1 WHERE transactionid ="+tid)
        s2 = c.fetchall()
        # print(s2)
        todo_array1 = []
        for t in s2:
            todo_array1.append(t)
        l1 = json.dumps(todo_array1[0])
        # print(l1)
        res1 = int(float(l1[1:-2]))

        val1 = int(res1)+int(amount)
        # print(val1)

        c.execute("UPDATE customer1 SET CURRENT=" +
                  str(val) + " WHERE transactionid="+str(ytid))

        c.execute("UPDATE customer1 SET CURRENT=" +
                  str(val1) + " WHERE transactionid="+str(tid))
        conn.commit()
        conn.close()
        return redirect('/viewallcust')


@app.route('/viewalltranc/<int:sno>')
def tranc_history(sno):
    conn = sqlite3.connect('bankdatabase.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM customer1 where sno=" + str(sno))
    cust = c.fetchall()
    c.execute(
        "SELECT * FROM transferhistorys WHERE yourid in (SELECT transactionid FROM customer1 WHERE sno=" + str(sno)+")")
    hist = c.fetchall()
    # print(hist)
    conn.commit()
    conn.close()
    return render_template('tranc_history.html', cust=cust, hist=hist)


@app.route('/viewalltranc')
def all_tranc_history():
    conn = sqlite3.connect('bankdatabase.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM transferhistorys")
    cust = c.fetchall()
    # print(hist)
    conn.commit()
    conn.close()
    return render_template('all_tranc_history.html', cust=cust)


if __name__ == "__main__":
    app.run(debug=True)
