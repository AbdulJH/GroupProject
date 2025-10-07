from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(f"Username: {username}, Password: {password}")
        return render_template("register.html")
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
