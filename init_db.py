import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATABASE_PATH = ROOT / "database" / "stikertrak.db"
SCHEMA_PATH = ROOT / "database" / "schema.sql"
SEED_PATH = ROOT / "database" / "seed.sql"


def initialize_database(reset=False):
    if DATABASE_PATH.exists() and reset:
        DATABASE_PATH.unlink()

    if DATABASE_PATH.exists():
        print("Database already exists.")
        return

    connection = sqlite3.connect(DATABASE_PATH)

    connection.executescript(SCHEMA_PATH.read_text())
    connection.executescript(SEED_PATH.read_text())

    connection.commit()
    connection.close()

    print("Database created successfully.")


if __name__ == "__main__":
    initialize_database(reset=True)