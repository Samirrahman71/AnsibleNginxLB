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
        
        # Load balancer method status endpoint
        if path == '/lb-status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow cross-origin requests
            self.end_headers()
            
            # In a real-world scenario, this would check the actual NGINX configuration
            # For demo purposes, we'll just return the default method
            # This could be enhanced to read the actual config or store the method in a shared state
            
            # Try to get the X-Load-Balancing-Method header from the request if NGINX passed it
            lb_method = self.headers.get('X-Load-Balancing-Method', 'Round Robin')
            
            # Map the header value to our method names
            method_map = {
                'Round Robin': 'round-robin',
                'Least Connections': 'least-connections',
                'IP Hash': 'ip-hash'
            }
            
            # Get the method from the map or default to round-robin
            method = method_map.get(lb_method, 'round-robin')
            
            # Get descriptions for each method
            descriptions = {
                'round-robin': 'Distributes requests sequentially across all servers',
                'least-connections': 'Routes to servers with fewest active connections',
                'ip-hash': 'Routes users from the same IP address to the same server (session persistence)'
            }
            
            # Send the response
            lb_data = f'{{"method":"{method}","description":"{descriptions.get(method)}","server":"{os.environ.get("APP_NAME", "app")}","requests":{LoadBalancerDemo.request_count}}}'
            self.wfile.write(lb_data.encode())
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
