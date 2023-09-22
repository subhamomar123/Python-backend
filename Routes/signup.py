import json
import random

def handle_signup(request_body, db_connection, db_cursor):
    try:
        request_data = json.loads(request_body)
        email, password = request_data.get("email"), request_data.get("password")
        sql = "INSERT INTO user_details (email, password) VALUES (%s, %s)"
        values = (email, password)
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

        return json.dumps({"message": "User registered successfully.", "status": "OK"})

    except json.JSONDecodeError as json_err:
        return json.dumps({"message": f"JSON Parsing Error: {json_err}", "status": "Error"})
    except Exception as e:
        return json.dumps({"message": f"An error occurred: {e}", "status": "Error"})
