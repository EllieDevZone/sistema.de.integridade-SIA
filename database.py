from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = str(BASE_DIR / "audit.db")


def create_database(db_name: str = DB_NAME) -> None:
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitored_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL UNIQUE,
            sha256_hash TEXT NOT NULL,
            registered_at TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()


def register_file(file_path: str, file_hash: str, timestamp: str, db_name: str = DB_NAME) -> bool:
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO monitored_files (file_path, sha256_hash, registered_at) VALUES (?, ?, ?)",
            (file_path, file_hash, timestamp),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def get_all_files(db_name: str = DB_NAME) -> list:
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT id, file_path, sha256_hash, registered_at FROM monitored_files ORDER BY file_path")
    rows = cursor.fetchall()
    connection.close()
    return rows


def update_file_hash(file_path: str, new_hash: str, timestamp: str, db_name: str = DB_NAME) -> None:
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE monitored_files SET sha256_hash = ?, registered_at = ? WHERE file_path = ?",
        (new_hash, timestamp, file_path),
    )
    connection.commit()
    connection.close()


def delete_all_files(db_name: str = DB_NAME) -> None:
    connection = sqlite3.connect(db_name)
    connection.execute("DELETE FROM monitored_files")
    connection.commit()
    connection.close()
