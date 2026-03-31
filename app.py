from flask import Flask, render_template,request,session,redirect
import sqlite3


app = Flask(__name__)
app.secret_key = "abc123"


@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login",methods = ["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "admin" and password == "1234":
        session["user"] = username
        return redirect("/dashboard")
    else:
        return "invalid login"

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html",user = session["user"])
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/")

@app.route("/profile")
def profile():
    if "user" in session:
        return render_template("profile.html")
    else:
        return redirect("/")

@app.route("/add")
def add():
    if "user" in session:
        return render_template("add.html")
    else:
        return redirect("/")

@app.route("/save",methods = ["POST"])
def save():
    if "user" not in session:
        return redirect("/")
    name = request.form.get("name")
    m1 = int(request.form.get("mark1" ))
    m2 = int(request.form.get("mark2" ))
    m3 = int(request.form.get("mark3" ))

    total = m1 + m2 + m3
    percent = round( total /3 ,2)

    if percent >= 80:
        grade = "A"
    elif percent >= 60:
        grade = "B"
    elif percent >= 40:
        grade = "C"
    else:
        grade = "F"

    if percent >= 40:
        status = "Pass"
    else:
        status = "Fail"

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, total, percent, grade, status) VALUES (?, ?, ?, ?, ?)",
        (name, total, percent, grade, status)
    )

    conn.commit()
    conn.close()
    return redirect("/view")

@app.route("/view")
def view():
    if "user" in session:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        conn.close()
        return render_template("view.html", students=students)


    else:
        return redirect("/")

@app.route("/clear")
def clear():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students")

    conn.commit()
    conn.close()

    return redirect("/view")

if __name__=="__main__":
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        total INTEGER,
        percent REAL,
        grade TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
    app.run(debug=True)



