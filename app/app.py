import os
import time
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import mimetypes
import urllib.parse

# Add common MIME types
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('image/svg+xml', '.svg')

class LoadBalancerDemo(BaseHTTPRequestHandler):
    start_time = time.time()
    request_count = 0
    
    def do_GET(self):
        # Parse the path
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Health check endpoint for APIs
        if path == '/health' or path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            uptime = int(time.time() - LoadBalancerDemo.start_time)
            hostname = os.environ.get('APP_NAME', 'app')
            health_data = f'{{"status":"healthy","server":"{hostname}","uptime":{uptime},"requests":{LoadBalancerDemo.request_count}}}'
            self.wfile.write(health_data.encode())
            return
        
        # Serve static files
        if path.startswith('/static/'):
            self.serve_static_file(path[8:])
            return
            
        # Serve the main page
        LoadBalancerDemo.request_count += 1
        hostname = os.environ.get('APP_NAME', 'app')
        
        # Read the template
        try:
            with open('templates/index.html', 'r') as file:
                content = file.read()
                
            # Replace placeholders with actual values
            content = content.replace('{{server_name}}', hostname)
            content = content.replace('{{timestamp}}', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            content = content.replace('{{uptime}}', str(int(time.time() - LoadBalancerDemo.start_time)))
            content = content.replace('{{request_count}}', str(LoadBalancerDemo.request_count))
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode())
            
        except FileNotFoundError:
            # Fallback to simple text if template is not found
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Hello from {hostname}!\n".encode())
            self.wfile.write(f"This server has handled {LoadBalancerDemo.request_count} requests since starting.\n".encode())
    
    def serve_static_file(self, file_path):
        try:
            with open(f'static/{file_path}', 'rb') as file:
                content = file.read()
                
            self.send_response(200)
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type:
                self.send_header('Content-type', content_type)
            else:
                self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            self.wfile.write(content)
            
        except FileNotFoundError:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'File not found')

if __name__ == "__main__":
    port = 8000
    server = HTTPServer(("0.0.0.0", port), LoadBalancerDemo)
    print(f"Serving demo on port {port}")
    server.serve_forever()
