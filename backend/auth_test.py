import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent.parent)

from auth_helper import register_user, login_user
from db_helpers import (
    add_or_update_sticker,
    get_collection_progress,
    get_user_collection,
    get_duplicate_stickers
)

try:
    user_id = register_user(
        username="testuser",
        email="test@example.com",
        password="Password123",
        first_name="Test",
        last_name="User"
    )

    print("User registered successfully.")
    print("New user ID:", user_id)

except ValueError as error:
    print("Registration note:", error)


user = login_user("test@example.com", "Password123")

if user is None:
    print("Login failed.")

else:
    print("Login successful.")
    print("User ID:", user["id"])

    print(add_or_update_sticker(user["id"], "MEX-04"))
    print(add_or_update_sticker(user["id"], "MEX-04"))

    progress = get_collection_progress(user["id"])

    print("Total stickers:", progress[0])
    print("Collected stickers:", progress[1])
    print("Missing stickers:", progress[2])
    print("Completion percentage:", progress[3], "%")

    print("Collection:")
for sticker in get_user_collection(user["id"]):
    print(sticker)

print("Duplicates:")
for duplicate in get_duplicate_stickers(user["id"]):
    print(duplicate)