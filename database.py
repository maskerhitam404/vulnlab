import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "vulnlab.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.executescript(
        """
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS comments;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS progress;

        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            secret_note TEXT
        );

        CREATE TABLE comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_scope TEXT NOT NULL,
            author TEXT NOT NULL,
            body TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        );

        CREATE TABLE progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_slug TEXT NOT NULL,
            level TEXT NOT NULL,
            solved_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(category_slug, level)
        );
        """
    )

    # Seed users - sengaja pakai password plaintext untuk keperluan lab SQLi
    cur.executemany(
        "INSERT INTO users (username, password, role, secret_note) VALUES (?, ?, ?, ?)",
        [
            ("administrator", "S3cr3tAdminPass!", "admin", "FLAG{sql_injection_apprentice_ok}"),
            ("carlos", "montoya123", "user", None),
            ("wiener", "peterpeter", "user", None),
        ],
    )

    cur.executemany(
        "INSERT INTO products (name, price, description) VALUES (?, ?, ?)",
        [
            ("Giant Enter Key", 9.25, "Satisfying mechanical enter key, extra large."),
            ("Trust Us t-shirt", 12.00, "For the security-conscious dresser."),
            ("Lightbulb Moment Notebook", 6.50, "For all your 'aha' vulnerability findings."),
        ],
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized at", DB_PATH)
