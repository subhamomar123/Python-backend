import json

def handle_base_route():
    response_data = {
        "message": "This is the base route. Hello world",
        "status": "OK"
    }
    return json.dumps(response_data)