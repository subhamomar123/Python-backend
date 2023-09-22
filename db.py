import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "python_crud"
}

def connect_to_database():
    try:
        db_connection = mysql.connector.connect(**db_config)
        db_cursor = db_connection.cursor()
        print("Connected to MySQL database successfully.")
        return db_connection, db_cursor
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None
