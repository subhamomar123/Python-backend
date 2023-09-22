import json

def handle_signup(request_body, db_connection, db_cursor):
    try:
        request_data = json.loads(request_body)
        email = request_data.get("email")
        password = request_data.get("password")

        sql = "INSERT INTO user_details ( email, password) VALUES ( %s, %s)"
        values = (email, password)
        db_cursor.execute(sql, values)
        db_connection.commit()

        response_data = {
            "message": "User registered successfully.",
            "status": "OK"
        }

        return json.dumps(response_data)

    except json.JSONDecodeError as json_err:
        error_message = f"JSON Parsing Error: {json_err}"
        response_data = {
            "message": error_message,
            "status": "Error"
        }
        return json.dumps(response_data)

    except Exception as e:
        error_message = f"An error occurred: {e}"
        response_data = {
            "message": error_message,
            "status": "Error"
        }
        return json.dumps(response_data)
