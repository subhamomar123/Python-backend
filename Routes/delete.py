import json
import globals
import jwt

def handle_delete(authorization_header, db_connection, db_cursor):
    try:
        jwt_token = authorization_header
        secret_key = globals.SECRET_KEY
        decoded_payload = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
        user_id = decoded_payload.get('id')

        if user_id is not None:
            sql = "DELETE FROM user_details WHERE id = %s"
            values = (user_id,)
            db_cursor.execute(sql, values)
            db_connection.commit()
            response_data = {
                'message': 'Delete successful'
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