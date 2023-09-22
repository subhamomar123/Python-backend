import json
import jwt

def handle_login(request_body, db_connection, db_cursor):
    try:
        request_data = json.loads(request_body)
        email = request_data.get("email")
        password = request_data.get("password")

        db_cursor.execute("SELECT id, password, jwt FROM user_details WHERE email = %s", (email,))
        user_data = db_cursor.fetchone()
        SECRET_KEY = "helloworld"
        if user_data and password == user_data[1]:
            payload = {
                'email': email
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            update_sql = "UPDATE user_details SET jwt = %s WHERE email = %s"
            update_values = (token, email)
            db_cursor.execute(update_sql, update_values)
            db_connection.commit()

            response_data = {
                'message': 'Login successful',
                'token': token
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
