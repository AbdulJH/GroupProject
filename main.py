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

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        insert_user(username, password)
        print(f"Username: {username}, Password: {password}")
        return render_template("register.html")
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
