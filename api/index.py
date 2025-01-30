import json
from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Parse query parameters
        query = self.path.split('?')[-1]
        names = [param.split('=')[-1] for param in query.split('&') if 'name=' in param]
        
        try:
            with open('q-vercel-python.json', 'r') as file:
                data = json.load(file)
        except Exception as e:
            self.wfile.write(json.dumps({"error": "Failed to load data", "details": str(e)}).encode('utf-8'))
            return
        
        # Get marks for provided names
        marks = [data.get(name, 0) for name in names]
        response = {"marks": marks}
        
        # Respond with JSON
        self.wfile.write(json.dumps(response).encode('utf-8'))
