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
    m1 = int(request.form.get("mark1" )or 0)
    m2 = int(request.form.get("mark2" )or 0)
    m3 = int(request.form.get("mark3" )or 0)

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

    students = {
        "name": name,
        "total":total,
        "percent":percent,
        "grade":grade,
        "status":status
    }

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, total, percent, grade, status) VALUES (:name, :total, :percent, :grade, :status)",
        students


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
        rows = cursor.fetchall()

        conn.close()

        students = []

        for r in rows:
            student = {
                "id": r[0],
                "name": r[1],
                "total": r[2],
                "percent": r[3],
                "grade": r[4],
                "status": r[5]
            }
            students.append(student)

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

@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/view")

@app.route("/edit/<int:id>")
def edit(id):
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
    row = cursor.fetchone()

    conn.close()

    student = {
        "id": row[0],
        "name": row[1],
        "total": row[2],
        "percent": row[3],
        "grade": row[4],
        "status": row[5]
    }

    return render_template("edit.html", student=student)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    if "user" not in session:
        return redirect("/")

    name = request.form.get("name")
    m1 = int(request.form.get("mark1") or 0)
    m2 = int(request.form.get("mark2") or 0)
    m3 = int(request.form.get("mark3") or 0)

    total = m1 + m2 + m3
    percent = round(total / 3, 2)

    if percent >= 80:
        grade = "A"
    elif percent >= 60:
        grade = "B"
    elif percent >= 40:
        grade = "C"
    else:
        grade = "F"

    status = "Pass" if percent >= 40 else "Fail"

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET name=?, total=?, percent=?, grade=?, status=?
        WHERE id=?
    """, (name, total, percent, grade, status, id))

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



