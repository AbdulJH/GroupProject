from flask import Flask, request, render_template, url_for, redirect
from database import insert_user, check_user, valid_login

app = Flask(__name__)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check_user(username):
            return render_template("register.html", username_taken=True)
        insert_user(username, password)
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not valid_login(username, password):
            return render_template("login.html", login_failed=True)
        return redirect(url_for("pdf2quizhome"))
    return render_template("login.html")

@app.route("/pdf2quizhome", methods=["GET"])
def pdf2quizhome():
    return render_template("pdf2quizhome.html")

if __name__ == "__main__":
    app.run(debug=True)
