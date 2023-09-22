import json

def handle_delete(authorization_header, db_connection, db_cursor):
    try:
        jwt = authorization_header

        db_cursor.execute("SELECT id FROM user_details WHERE jwt = %s", (jwt,))

        user_id = db_cursor.fetchone()
        if user_id is not None :
            sql = "DELETE FROM user_details WHERE id = %s"
            values = (user_id[0],)
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
