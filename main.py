import http.server
import socketserver
from urllib import request
from os import getenv
import json

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        """Respond to a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        try:
            result = request.urlopen(coordinates_url)
            data = json.load(result)
        except Exception as e:
            print(e)
            data = {'altitude': 'None', 'latitude': 'None'}

        self.wfile.write(bytes("<html><head><title>Title goes here.</title></head>", "utf-8"))
        self.wfile.write(bytes(f"<body><p>altitude: {data['altitude']} latitude: {data['latitude']}</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))



PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

coordinates_url = getenv('COORDINATES_URL')

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()