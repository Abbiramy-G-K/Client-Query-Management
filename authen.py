import hashlib
import mysql.connector



def authenticate(username, password, conn, salt):
    username = username.strip()
    print("RAW PASSWORD INPUT:", repr(password))  
    password = password.strip()
    hashed_pw = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    print("HASHED PASSWORD:", hashed_pw)

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE TRIM(username)=%s AND password=%s",
        (username, hashed_pw)
    )
    user = cursor.fetchone()
    cursor.close()
    print("DB RESULT:", user)
    return user

