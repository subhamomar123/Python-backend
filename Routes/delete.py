import json
import jwt

def handle_delete(request_body, db_connection, db_cursor):
    try:
        request_data = json.loads(request_body)
        jwt = request_data.get("jwt")

        db_cursor.execute("SELECT id FROM user_details WHERE jwt = %s", (jwt,))
        user_id = db_cursor.fetchone()
        SECRET_KEY = "helloworld"
        if len(user_id) :
            sql = "DELETE FROM user_details WHERE id = %s"
            values = (user_id)
            db_cursor.execute(sql, values)
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
