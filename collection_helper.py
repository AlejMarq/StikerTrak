from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from db_helpers import add_or_update_sticker
from db_helpers import get_collection_progress
from db_helpers import get_duplicate_stickers
from db_helpers import get_missing_stickers
from db_helpers import get_user_collection


collection_routes = Blueprint("collection_routes", __name__)

# Temporary user id for testing
# This will later be replaced with the logged-in user's id
TEST_USER_ID = 1


@collection_routes.route("/collection")
def show_collection():
    """
    Displays the user's collection information.
    """

    owned_stickers = get_user_collection(TEST_USER_ID)
    missing_stickers = get_missing_stickers(TEST_USER_ID)
    duplicate_stickers = get_duplicate_stickers(TEST_USER_ID)
    progress = get_collection_progress(TEST_USER_ID)

    return render_template(
        "collection.html",
        owned_stickers=owned_stickers,
        missing_stickers=missing_stickers,
        duplicate_stickers=duplicate_stickers,
        progress=progress
    )


@collection_routes.route("/collection/add", methods=["POST"])
def add_sticker():
    """
    Adds a sticker to the user's collection.
    """

    sticker_number = request.form.get("sticker_number")

    if sticker_number is None:
        return redirect(url_for("collection_routes.show_collection"))

    sticker_number = sticker_number.strip().upper()

    if sticker_number == "":
        return redirect(url_for("collection_routes.show_collection"))

    add_or_update_sticker(TEST_USER_ID, sticker_number)

    return redirect(url_for("collection_routes.show_collection"))
