import http.server
from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse
import importlib
from db import connect_to_database

db_connection, db_cursor = connect_to_database()

class MyHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        url_parts = urlparse(self.path)
        path = url_parts.path
        response = ""
        status_code = 200
            
        if path == '/signup':
            module = importlib.import_module('Routes.signup')
            response, status_code = module.handle_signup(self.rfile.read(int(self.headers['Content-Length'])), db_connection, db_cursor)
        elif path == '/login':  
            module = importlib.import_module('Routes.login')
            response, status_code = module.handle_login(self.rfile.read(int(self.headers['Content-Length'])), db_connection, db_cursor)
        elif path == '/change_password':
            module = importlib.import_module('Routes.change_password')
            response, status_code = module.handle_change_password(self.rfile.read(int(self.headers['Content-Length'])), db_connection, db_cursor)
            
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))


    def do_GET(self):
        url_parts = urlparse(self.path)
        path = url_parts.path
        
        if path == '/':
            module = importlib.import_module('Routes.Base_route')
            response = module.handle_base_route()
        elif path == '/delete':
            module = importlib.import_module('Routes.delete')
            response = module.handle_delete(self.headers['Authorization'], db_connection, db_cursor)
        elif path == '/courses':
            module = importlib.import_module('Routes.courses')
            response = module.display_user_courses(self.headers['Authorization'], db_connection, db_cursor)


        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

port = 8000
handler = MyHandler

with http.server.HTTPServer(("", port), handler) as httpd:
    print(f"Serving on port {port}...")
    httpd.serve_forever()