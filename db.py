import mysql.connector
from globals import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

def connect_to_database():
    try:
        db_config = {
            "host": DB_HOST,
            "user": DB_USER,
            "password": DB_PASSWORD,
            "database": DB_DATABASE
        }
        db_connection = mysql.connector.connect(**db_config) #holds state of current connection
        db_cursor = db_connection.cursor()
        print("Connected to MySQL database successfully.")
        return db_connection, db_cursor
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None
