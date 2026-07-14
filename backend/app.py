from flask import Flask, render_template

app = Flask(__name__, static_folder="../frontend", static_url_path="/frontend")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/collection")
def collection():
    return render_template("collection.html")

if __name__ == "__main__":
    app.run(debug=True)