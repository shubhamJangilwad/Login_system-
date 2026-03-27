from flask import Flask, render_template,request,session,redirect

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
        return "This is profile page"
    else:
        return redirect("/")

if __name__=="__main__":
    app.run(debug=True)


