import sqlite3

DATABASE_PATH = "database/stikertrak.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def get_all_stickers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT sticker_number, category, section, name, country
        FROM stickers
        ORDER BY sticker_number;
    """)

    stickers = cursor.fetchall()

    connection.close()

    return stickers

def get_stickers_by_country(country):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT sticker_number, category, section, name, country
        FROM stickers
        WHERE country = ?
        ORDER BY sticker_number;
    """, (country,))

    stickers = cursor.fetchall()

    connection.close()

    return stickers

def get_sticker_by_number(sticker_number):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT sticker_number, category, section, name, country
        FROM stickers
        WHERE sticker_number = ?;
    """, (sticker_number,))

    sticker = cursor.fetchone()

    connection.close()

    return sticker

def add_or_update_sticker(user_id, sticker_number):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM stickers
        WHERE sticker_number = ?;
    """, (sticker_number,))

    sticker = cursor.fetchone()

    if sticker is None:
        connection.close()
        return "Sticker not found."

    sticker_id = sticker[0]

    cursor.execute("""
        SELECT quantity
        FROM user_collection
        WHERE user_id = ? AND sticker_id = ?;
    """, (user_id, sticker_id))

    collection_item = cursor.fetchone()

    if collection_item is None:
        cursor.execute("""
            INSERT INTO user_collection (user_id, sticker_id, quantity)
            VALUES (?, ?, 1);
        """, (user_id, sticker_id))

        message = "Sticker added to collection."
    else:
        new_quantity = collection_item[0] + 1

        cursor.execute("""
            UPDATE user_collection
            SET quantity = ?
            WHERE user_id = ? AND sticker_id = ?;
        """, (new_quantity, user_id, sticker_id))

        duplicates = new_quantity - 1
        message = f"Duplicate sticker. You now have {duplicates} duplicate(s)."

    connection.commit()
    connection.close()

    return message

def get_user_collection(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            stickers.sticker_number,
            stickers.category,
            stickers.section,
            stickers.name,
            stickers.country,
            user_collection.quantity
        FROM user_collection
        JOIN stickers ON user_collection.sticker_id = stickers.id
        WHERE user_collection.user_id = ?
        ORDER BY stickers.sticker_number;
    """, (user_id,))

    collection = cursor.fetchall()

    connection.close()

    return collection

def get_duplicate_stickers(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            stickers.sticker_number,
            stickers.category,
            stickers.section,
            stickers.name,
            stickers.country,
            user_collection.quantity
        FROM user_collection
        JOIN stickers ON user_collection.sticker_id = stickers.id
        WHERE user_collection.user_id = ?
        AND user_collection.quantity > 1
        ORDER BY stickers.sticker_number;
    """, (user_id,))

    duplicates = cursor.fetchall()

    connection.close()

    return duplicates

def get_missing_stickers(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            stickers.sticker_number,
            stickers.category,
            stickers.section,
            stickers.name,
            stickers.country
        FROM stickers
        WHERE stickers.id NOT IN (
            SELECT sticker_id
            FROM user_collection
            WHERE user_id = ?
        )
        ORDER BY stickers.sticker_number;
    """, (user_id,))

    missing = cursor.fetchall()

    connection.close()

    return missing

def get_collection_progress(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM stickers;
    """)
    total_stickers = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM user_collection
        WHERE user_id = ? AND quantity > 0;
    """, (user_id,))
    collected_stickers = cursor.fetchone()[0]

    missing_stickers = total_stickers - collected_stickers

    if total_stickers == 0:
        completion_percentage = 0
    else:
        completion_percentage = round((collected_stickers / total_stickers) * 100, 2)

    connection.close()

    return total_stickers, collected_stickers, missing_stickers, completion_percentage