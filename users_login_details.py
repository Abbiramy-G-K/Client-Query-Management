import os
import pandas as pd
import hashlib
import mysql.connector

df = pd.read_excel(r"C:/Users/abbir/OneDrive/Documents/Client Query Management/users.xlsx")
passwords = df['password']

print("RAW EXCEL PASSWORDS:")
for p in df['password']:
    print(repr(p)) 



salt = "random_salt_values"

test_pw = "pass01"
print("TEST HASH:", hashlib.sha256((test_pw + salt).encode()).hexdigest())


df['password'] = df['password'].apply(
    lambda p: str(p).split('.')[0].strip() if isinstance(p, (int, float)) else str(p).strip()
)


df['password'] = df['password'].apply(
    lambda p: hashlib.sha256((p + salt).encode('utf-8')).hexdigest()
)

conn = mysql.connector.connect(
    host="localhost",
    port = 3306,
    user="root",              
    password="Abbivimi@7", 
    database="user_management"
)

cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(50) NOT NULL,
#     password VARCHAR(255) NOT NULL,
#     role VARCHAR(50) NOT NULL
# )
# """)

insert_query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"

for row in df.itertuples(index=False):
    print("INSERT DEBUG:", row.username, row.password) 
    cursor.execute(insert_query, (row.username, row.password, row.role))
conn.commit()
cursor.close()
conn.close()

