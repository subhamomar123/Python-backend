import json
import random
import bcrypt

def handle_signup(request_body, db_connection, db_cursor):
    try:
        request_data = json.loads(request_body)
        email, password = request_data.get("email"), request_data.get("password")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        sql = "INSERT INTO user_details (email, password) VALUES (%s, %s)"
        values = (email, hashed_password)
        db_cursor.execute(sql, values)

        db_connection.commit()
        db_cursor.execute("SELECT id FROM user_details WHERE email = %s", (email,))
        user_id = db_cursor.fetchone()

        db_cursor.execute("SELECT id FROM courses_list")
        id_list = [row[0] for row in db_cursor.fetchall()]
        user_courses = random.sample(id_list, 5)

        for course_id in user_courses:
            sql = "INSERT INTO user_courses (user_id, course_id) VALUES (%s, %s)"
            values = (user_id[0], course_id)
            db_cursor.execute(sql, values)

        db_connection.commit()

        response = {"message": "User registered successfully.", "status": "OK"}
        return json.dumps(response), 200

    except json.JSONDecodeError as json_err:
        response = {"message": f"JSON Parsing Error: {json_err}", "status": "Error"}
        return json.dumps(response), 400
    except Exception as e:
        response = {"message": f"An error occurred: {e}", "status": "Error"}
        return json.dumps(response), 500
