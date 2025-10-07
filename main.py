import psycopg2
def insert_user(username, password):
    conn = psycopg2.connect(
        dbname="ics499db",
        user="postgres",
        password="",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, password)
    )
    conn.commit()
    cur.close()
    conn.close()

def check_user(username):
    conn = psycopg2.connect(
        dbname="ics499db",
        user="postgres",
        password="",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM users WHERE username = %s",
        (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user is not None

def valid_login(username, password):
    conn = psycopg2.connect(
        dbname="ics499db",
        user="postgres",
        password="",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM users WHERE username = %s AND password = %s",
        (username, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user is not None

    
# create a method username_taken to check dataase to see if username is already taken. if it is return true if its not return false 
# then in  register method we do if !username_taken(username):
# insert_user() else we return usernaem taken message or popup



from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check_user(username):
            return render_template("register.html", username_taken=True)
        insert_user(username, password)
        print(f"Username: {username}, Password: {password}")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not valid_login(username, password):
            return render_template("login.html", login_failed=True)
        print("Login Successful")
        return "Login successful!"
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
