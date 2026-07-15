from flask import Flask, render_template, request, redirect, session
from auth_helper import login_user, register_user

from db_helpers import (
    get_all_stickers,
    get_user_collection,
    get_collection_progress,
    get_duplicate_stickers,
    add_or_update_sticker,
    decrease_sticker_quantity,
)

app = Flask(__name__, static_folder="../frontend", static_url_path="/frontend")
app.secret_key = "stikertrak-dev-key"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form["username_or_email"]
        password = request.form["password"]

        user = login_user(username_or_email, password)

        if user is not None:
            session["user_id"] = user["id"]
            return redirect("/collection")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]

        try:
            user_id = register_user(
                username,
                email,
                password,
                first_name,
                last_name
            )

            session["user_id"] = user_id
            return redirect("/collection")
    
        except ValueError as error:
            return render_template("signup.html", signup_error=str(error))

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/collection")
def collection():
    if "user_id" not in session:
        return redirect("/login")
    
    user_id = session.get("user_id")

    all_stickers = get_all_stickers()
    collection_data = get_user_collection(user_id)
    progress = get_collection_progress(user_id)
    duplicates = get_duplicate_stickers(user_id)

    owned_stickers = {
    item[0]: item[5]
    for item in collection_data
}

    print(collection_data)

    return render_template(
        "collection.html",
        stickers=all_stickers,
        collection=collection_data,
        owned_stickers=owned_stickers,
        progress=progress,
        duplicates=duplicates
    )

@app.route("/add-sticker/<sticker_number>", methods=["POST"])
def add_sticker(sticker_number):
    user_id = session.get("user_id")
    add_or_update_sticker(user_id, sticker_number)

    return redirect("/collection")

@app.route("/decrease-sticker/<sticker_number>", methods=["POST"])
def decrease_sticker(sticker_number):
    user_id = session.get("user_id")
    decrease_sticker_quantity(user_id, sticker_number)

    return redirect("/collection")

if __name__ == "__main__":
    app.run(debug=True)