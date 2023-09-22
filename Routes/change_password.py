import json
import bcrypt
import jwt
import globals

def handle_change_password(request_body, db_connection, db_cursor):
    try:
        secret_key = globals.SECRET_KEY
        request_data = json.loads(request_body)
        jwt_token = request_data.get("jwt")  # Change variable name to avoid conflict
        new_password = request_data.get("new_password")

        decoded_token = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])  # Use PyJWT to decode the token
        user_id = decoded_token.get('id')

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)

        db_cursor.execute("UPDATE user_details SET password = %s WHERE id = %s", (hashed_password, user_id))
        db_connection.commit()

        return json.dumps({'message': 'Password changed successfully'}), 200

    except json.JSONDecodeError as json_err:
        return json.dumps({'message': f'JSON Parsing Error: {json_err}', 'status': 'Error'}), 400

    except jwt.ExpiredSignatureError:
        return json.dumps({'message': 'Token has expired', 'status': 'Error'}), 401

    except jwt.InvalidTokenError:
        return json.dumps({'message': 'Invalid token', 'status': 'Error'}), 401

    except Exception as e:
        return json.dumps({'message': f'Error: {str(e)}', 'status': 'Error'}), 500
