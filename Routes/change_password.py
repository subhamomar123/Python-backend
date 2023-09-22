import json

def handle_change_password(request_body, db_connection, db_cursor):
    try:
        request_data = json.loads(request_body)
        jwt = request_data.get("jwt")
        password = request_data.get("password")

        db_cursor.execute("SELECT password FROM user_details WHERE jwt = %s", (jwt,))
        user_password = db_cursor.fetchone()
        if password is not None and user_password is not None:
            update_sql = "UPDATE user_details SET password = %s WHERE jwt = %s"
            update_values = (password, jwt)
            db_cursor.execute(update_sql, update_values)
            db_connection.commit()
            response_data = {
                'message': 'Password changed successfully'
            }
            return json.dumps(response_data)
        else:
            response_data = {
                "message": "Invalid credentials",
                "status": "Error"
            }
            return json.dumps(response_data)

    except Exception as e:
        response_data = {
            'message': f'Error: {str(e)}'
        }
        return json.dumps(response_data)
