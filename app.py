from flask import Flask, redirect, request, render_template, url_for, session
import psycopg2
import os
from urllib.parse import urlparse


app = Flask(__name__)


# Render-এ Secret Key এনভায়রনমেন্ট ভেরিয়েবল থেকে নেবে, না থাকলে ডিফল্ট 'supersecret'
app.secret_key = os.environ.get("SECRET_KEY", "supersecret")


# Render-এর ড্যাশবোর্ড থেকে DATABASE_URL রিড করা
DATABASE_URL = os.environ.get("DATABASE_URL")


# 👉 DB connection function
def get_db_connection():
    try:
        if DATABASE_URL:
            # Render PostgreSQL-এর জন্য sslmode='require' অবশ্যই প্রয়োজন
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:
            # এটি আপনার লোকাল কম্পিউটারে কাজ করার জন্য
            conn = psycopg2.connect(
                host="localhost",
                database="skydb",
                user="postgres",
                password="Manir@2005",
                port="5432"
            )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')


        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute(
                    "INSERT INTO users(name, email, password) VALUES(%s, %s, %s)",
                    (name, email, password)
                )
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('login'))
            except Exception as e:
                return f"Signup Error: {e}"
        else:
            return "Database connection failed!"


    return render_template('signup.html')


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')


        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM users WHERE email=%s AND password=%s",
                (email, password)
            )
            user = cur.fetchone()
            cur.close()
            conn.close()


            if user:
                session['name'] = user[1]
                return redirect(url_for('student_form'))
            else:
                return "Email or password wrong!"
        else:
            return "Database connection failed!"


    return render_template('login.html')


@app.route('/student_form', methods=["GET", "POST"])
def student_form():
    if request.method == "POST":
        name = request.form.get('Full name')
        college = request.form.get('college name')
        department = request.form.get('Department')
        email = request.form.get('email')
        student_code = request.form.get('student code')
        location = request.form.get('location')
        pass_year = request.form.get('year of passing')


        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute(
                    """INSERT INTO students(name, college, department, email, student_code, location, pass_year)
                       VALUES(%s, %s, %s, %s, %s, %s, %s)""",
                    (name, college, department, email, student_code, location, pass_year)
                )
                conn.commit()
                cur.close()
                conn.close()
                return 'Submitted successfully!'
            except Exception as e:
                return f"Form Submission Error: {e}"
        else:
            return "Database connection failed!"


    return render_template('student_form.html')


if __name__ == '__main__':
    # Render-এর ডাইনামিক পোর্ট হ্যান্ডেল করার জন্য
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

