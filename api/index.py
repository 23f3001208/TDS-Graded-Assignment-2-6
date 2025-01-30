import json
from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')  # Allow all methods
        self.send_header('Access-Control-Allow-Headers', '*')  # Allow all headers
        self.end_headers()
        
        # Parse query parameters
        query = self.path.split('?')[-1]
        names = [param.split('=')[-1] for param in query.split('&') if 'name=' in param]
        
        try:
            file_path = os.path.join(os.path.dirname(__file__), 'q-vercel-python.json')
            with open(file_path, 'r') as file:
                data = json.load(file)
        except Exception as e:
            self.wfile.write(json.dumps({"error": "Failed to load data", "details": str(e)}).encode('utf-8'))
            return
        
        # Get marks for provided names
        marks = []
        for name in names:
            # Assuming each item in data is a dictionary with a 'name' key
            mark = 0
            for entry in data:
                if entry.get('name') == name:
                    mark = entry.get('marks', 0)  # Assuming 'marks' key exists in each dictionary
                    break
            marks.append(mark)
        response = {"marks": marks}
        
        # Respond with JSON
        self.wfile.write(json.dumps(response).encode('utf-8'))