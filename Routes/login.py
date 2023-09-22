import json
import jwt
import globals
import bcrypt

secret_key = globals.SECRET_KEY

def handle_login(request_body, db_connection, db_cursor):
    try:
        request_data = json.loads(request_body)
        email, password = request_data.get("email"), request_data.get("password")

        db_cursor.execute("SELECT id, password, email FROM user_details WHERE email = %s", (email,))
        user_data = db_cursor.fetchone()

        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[1].encode('utf-8')):
            payload = {
                'id': user_data[0],
                'email': user_data[2]
            }

            token = jwt.encode(payload, secret_key, algorithm='HS256')

            update_sql = "UPDATE user_details SET jwt = %s WHERE email = %s"
            update_values = (token, email)
            db_cursor.execute(update_sql, update_values)
            db_connection.commit()

            return json.dumps({'message': 'Login successful', 'token': token}), 200
        else:
            return json.dumps({"message": "Invalid credentials", "status": "Error"}), 401

    except Exception as e:
        return json.dumps({'message': f'Error: {str(e)}'}), 500
