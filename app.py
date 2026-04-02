from flask import Flask, redirect, request, render_template, url_for, session
import psycopg2
import os


app = Flask(__name__)
# Render-এর জন্য Secret Key এনভায়রনমেন্ট ভেরিয়েবল থেকে নেওয়া ভালো
app.secret_key = os.environ.get("SECRET_KEY", "supersecret")


# Render-এর ড্যাশবোর্ড থেকে DATABASE_URL রিড করা
DATABASE_URL = os.environ.get("DATABASE_URL")


# 👉 DB connection function
def get_db_connection():
    try:
        if DATABASE_URL:
            # Render PostgreSQL-এর জন্য sslmode='require' অবশ্যই লাগবে
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        else:
            # এটি আপনার লোকাল কম্পিউটারের জন্য
            conn = psycopg2.connect(
                host="localhost",
                database="skydb",
                user="postgres",
                password="Manir@2005",
                port="5432"
            )
        return conn
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return None


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']


        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users(name,email,password) VALUES(%s, %s, %s)",
                (name, email, password)
            )
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('login'))
        return "Database Connection Failed!"
    return render_template('signup.html')


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']


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
                return "email or password wrong!"
        return "Database Connection Failed!"
    return render_template('login.html')


@app.route('/student_form', methods=["GET", "POST"])
def student_form():
    if request.method == "POST":
        name = request.form['Full name']
        college = request.form['college name']
        department = request.form['Department']
        email = request.form['email']
        student_code = request.form['student code']
        location = request.form['location']
        pass_year = request.form['year of passing']


        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO students(name,college,department,email,student_code,location,pass_year)
                   VALUES(%s,%s,%s,%s,%s,%s,%s)""",
                (name, college, department, email, student_code, location, pass_year)
            )
            conn.commit()
            cur.close()
            conn.close()
            return 'your submit successfully!'
        return "Database Connection Failed!"
    return render_template('student_form.html')


if __name__ == '__main__':
    # Render-এর ডাইনামিক পোর্ট এবং হোস্ট সেটআপ (খুবই জরুরি)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

