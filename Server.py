import http.server
from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import importlib

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        url_parts = urlparse(self.path)
        path = url_parts.path
        query = parse_qs(url_parts.query)

        if path == '/':
            module = importlib.import_module('Routes.Base_route')
            response = module.handle_base_route()
        elif path == '/route1':
            module = importlib.import_module('Routes.route1')
            response = module.handle_route1()
        elif path == '/route2':
            module = importlib.import_module('Routes.route2')
            response = module.handle_route2()
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response_data = {
                "message": "Not Found",
                "status": "Error"
            }
            response = json.dumps(response_data)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))

port = 8000
handler = MyHandler

with http.server.HTTPServer(("", port), handler) as httpd:
    print(f"Serving on port {port}...")
    httpd.serve_forever()
