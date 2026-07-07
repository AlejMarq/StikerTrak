import hashlib
import hmac
import re
import secrets
import sqlite3

from db_helpers import get_connection

PBKDF2_ITERATIONS = 600_000

# Simple in-memory session storage for testing
# Key = session token, Value = user id
active_sessions = {}


def validate_password(password):
    """
    Checks if the password meets basic security requirements.
    Returns a list of errors if any
    """
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")

    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")

    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")

    if not re.search(r"[0-9]", password):
        errors.append("Password must contain at least one number.")

    return errors


def hash_password(password):
    """
    Hashes a password using PBKDF2 and a random salt.
    This means the real password is never stored in the database incase of hacks
    """
    salt = secrets.token_bytes(16)

    hashed_password = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS
    )

    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${hashed_password.hex()}"


def verify_password(password, stored_hash):
    """
    Checks if the entered password matches the stored password hash.
    """
    try:
        algorithm, iterations, salt_hex, expected_hash_hex = stored_hash.split("$")

        if algorithm != "pbkdf2_sha256":
            return False

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations)
        )

        expected_hash = bytes.fromhex(expected_hash_hex)

        return hmac.compare_digest(actual_hash, expected_hash)

    except Exception:
        return False


def register_user(username, email, password, first_name, last_name):
    """
    Creates a new user account.
    Returns the new user's id.
    Raises ValueError if the password is weak or username/email already exists.
    """
    password_errors = validate_password(password)

    if password_errors:
        raise ValueError(" ".join(password_errors))

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, first_name, last_name)
            VALUES (?, ?, ?, ?, ?);
            """,
            (
                username.strip(),
                email.lower().strip(),
                hash_password(password),
                first_name.strip(),
                last_name.strip()
            )
        )

        connection.commit()
        return cursor.lastrowid

    except sqlite3.IntegrityError:
        raise ValueError("Username or email already exists.")

    finally:
        connection.close()


def login_user(username_or_email, password):
    """
    Logs in a user using either username or email.
    Returns a user dictionary if successful.
    Returns None if login fails.
    """
    username_or_email = username_or_email.lower().strip()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username, email, password_hash, first_name, last_name
        FROM users
        WHERE lower(username) = ? OR lower(email) = ?;
        """,
        (username_or_email, username_or_email)
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None

    # The selected columns are:
    # row[0] = id
    # row[1] = username
    # row[2] = email
    # row[3] = password_hash
    # row[4] = first_name
    # row[5] = last_name
    if not verify_password(password, row[3]):
        return None

    return {
        "id": row[0],
        "username": row[1],
        "email": row[2],
        "first_name": row[4],
        "last_name": row[5]
    }


def create_session(user_id):
    """
    Creates a simple login session token for the user.
    """
    session_token = secrets.token_hex(32)
    active_sessions[session_token] = user_id
    return session_token


def get_current_user(session_token):
    """
    Gets the logged-in user from a session token.
    Returns None if the session does not exist.
    """
    user_id = active_sessions.get(session_token)

    if user_id is None:
        return None

    return get_user_by_id(user_id)


def logout_user(session_token):
    """
    Logs out a user by removing their session token.
    """
    if session_token in active_sessions:
        del active_sessions[session_token]
        return True

    return False


def get_user_by_id(user_id):
    """
    Finds a user by id.
    Returns a user dictionary or None.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username, email, first_name, last_name
        FROM users
        WHERE id = ?;
        """,
        (user_id,)
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "username": row[1],
        "email": row[2],
        "first_name": row[3],
        "last_name": row[4]
    }