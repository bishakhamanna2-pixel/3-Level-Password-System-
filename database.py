import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


DATABASE = "database.db"


# ===================================================
# DATABASE CONNECTION
# ===================================================

def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# ===================================================
# CREATE DATABASE
# ===================================================

def create_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            face_path TEXT
        )
    """)

    conn.commit()

    conn.close()


# ===================================================
# REGISTER USER
# ===================================================

def register_user(username, phone, password):

    conn = get_connection()

    cursor = conn.cursor()

    hashed_password = generate_password_hash(
        password
    )

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username, phone, password)
            VALUES (?, ?, ?)
            """,
            (
                username.strip(),
                phone.strip(),
                hashed_password,
            ),
        )

        conn.commit()

        user_id = cursor.lastrowid

        return user_id


    except sqlite3.IntegrityError:

        raise ValueError(
            "Username or phone number already registered."
        )


    finally:

        conn.close()


# ===================================================
# GET USER BY USERNAME
# ===================================================

def get_user(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username.strip(),)
    )

    user = cursor.fetchone()

    conn.close()

    return user


# ===================================================
# GET USER BY ID
# ===================================================

def get_user_by_id(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


# ===================================================
# VERIFY PASSWORD
# ===================================================

def verify_password(
    entered_password,
    stored_password
):

    return check_password_hash(
        stored_password,
        entered_password
    )


# ===================================================
# UPDATE FACE PATH
# ===================================================

def update_face_path(
    user_id,
    face_path
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET face_path = ?
        WHERE id = ?
        """,
        (
            face_path,
            user_id
        )
    )

    conn.commit()

    conn.close()


# ===================================================
# CHECK USERNAME
# ===================================================

def username_exists(username):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        (username.strip(),)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


# ===================================================
# CHECK PHONE NUMBER
# ===================================================

def phone_exists(phone):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE phone = ?
        """,
        (phone.strip(),)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


# ===================================================
# RUN DIRECTLY
# ===================================================

if __name__ == "__main__":

    create_database()

    print(
        "Database created successfully!"
    )