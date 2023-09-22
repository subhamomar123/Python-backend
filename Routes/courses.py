import json
import jwt
import globals

secret_key = globals.SECRET_KEY
def display_user_courses(authorization_header, db_connection, db_cursor):
    try:
        jwt_token = authorization_header
        try:
            decoded_payload = jwt.decode(jwt_token, secret_key, algorithms=['HS256'])
            print(decoded_payload)

            user_id = decoded_payload.get('id')

            sql = "SELECT cl.course_name FROM user_courses uc INNER JOIN courses_list cl ON uc.course_id = cl.id WHERE uc.user_id = %s"
            values = (user_id,)
            db_cursor.execute(sql,values)
            user_courses = db_cursor.fetchall()
            course_names = [row[0] for row in user_courses]

            return json.dumps({"Courses": course_names})
        except jwt.ExpiredSignatureError:
            return json.dumps({"message": "JWT has expired", "status": "Error"})
        except jwt.DecodeError:
            return json.dumps({"message": "Invalid JWT", "status": "Error"})

    except Exception as e:
        return json.dumps({'message': f'Error: {str(e)}'})
