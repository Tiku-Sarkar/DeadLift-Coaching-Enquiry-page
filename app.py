from flask import Flask, render_template, request, redirect
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "clients.db")
app =Flask(__name__)

with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS CONTACTS(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT,
                       email TEXT,
                       msg TEXT
                    )
            """)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/contact", methods =['POST'])
def form():
    
    name = request.form['name']
    email = request.form['email']
    msg = request.form['msg']
    if not name or not email or not msg:
        return redirect('/')
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO CONTACTS(name,email,msg) VALUES(?,?,?)',(name,email,msg))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route("/admin")
def printData():
    #  conn = sqlite3.connect('clients.db')
     conn = sqlite3.connect(DB_PATH)
     cursor = conn.cursor()
     cursor.execute('SELECT * FROM CONTACTS')
     clientData = cursor.fetchall()
     conn.close()
     return render_template("admin.html", data=clientData)

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM CONTACTS WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)