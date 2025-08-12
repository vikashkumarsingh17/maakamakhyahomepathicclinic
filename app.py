from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import qrcode
import os

app = Flask(__name__)
app.secret_key = "clinic_secret_key"
DB_NAME = "patients.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    phone TEXT,
                    address TEXT,
                    problem TEXT,
                    date TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        address = request.form['address']
        problem = request.form['problem']

        conn = sqlite3.connect('patients.db')
        c = conn.cursor()
        c.execute("INSERT INTO patients (name, age, gender, phone, address, date, problem) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (name, age, gender, phone, address, datetime.now().strftime("%Y-%m-%d %H:%M"), problem))
        patient_id = c.lastrowid
        conn.commit()
        conn.close()
        # return "Registration successful! Your patient ID is: {}".format(patient_id)
        return redirect(url_for("print_detail", patient_id=patient_id))
    return render_template("register.html")

@app.route("/register_new", methods=["GET", "POST"])
def register_new():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        address = request.form['address']
        problem = request.form['problem']

        conn = sqlite3.connect('patients.db')
        c = conn.cursor()
        c.execute("INSERT INTO patients (name, age, gender, phone, address, date, problem) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (name, age, gender, phone, address, datetime.now().strftime("%Y-%m-%d %H:%M"), problem))
        patient_id = c.lastrowid
        conn.commit()
        conn.close()
        # return "Registration successful! Your patient ID is: {}".format(patient_id)
        return "Registration successful! Your patient ID is: {}".format(patient_id)
    return render_template("new_registration.html")
@app.route("/print/<int:patient_id>")
def print_detail(patient_id):
    conn = sqlite3.connect('patients.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = c.fetchone()
    conn.close()
    return render_template("print_detail.html", patient=patient)
@app.route("/offlineRegister", methods=["GET", "POST"])
def offlineRegister():
    return render_template("offlineRegister.html")


@app.route('/list')
def list_patients():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM patients ORDER BY id DESC")
    patients = c.fetchall()
    conn.close()
    return render_template('list.html', patients=patients)

@app.route('/detaillist/<id>', methods=['GET', 'POST'])
def detail_list(id):
    patient = None
    if request.method == 'GET':
        # search = request.form['search']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM patients WHERE id=? ", (id,))
        patient = c.fetchall()
        conn.close()
    return render_template('detail.html', patient=patient)
@app.route('/detail', methods=['GET', 'POST'])
def detail():
    patient = None
    if request.method == 'POST':
        search = request.form['search']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM patients WHERE id=? OR name LIKE ?", (search, f"%{search}%"))
        patient = c.fetchall()
        conn.close()
    return render_template('detail.html', patient=patient)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Here you would typically check the username and password against a database
        if username == 'admin' and password == 'password':
            # flash('Login successful!', 'success')
            return render_template('homeReg.html')
        else:
            flash('Invalid credentials, please try again.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
