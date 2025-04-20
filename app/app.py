import os
from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        hostname = os.environ.get('APP_NAME', 'app')
        self.wfile.write(f"Hello from {hostname}!\n".encode())

if __name__ == "__main__":
    port = 8000
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"Serving on port {port}")
    server.serve_forever()
