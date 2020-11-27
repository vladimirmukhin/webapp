import http.server
import socketserver
import requests
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

        print(self.headers)

        try:
            headers = {
                'x-request-id'     : self.headers['x-request-id'],
                'x-b3-traceid'     : self.headers['x-b3-traceid'],
                'x-b3-spanid'      : self.headers['x-b3-spanid'],
                'x-b3-parentspanid': self.headers['x-b3-parentspanid'],
                'x-b3-sampled'     : self.headers['x-b3-sampled'],
                'x-b3-flags'       : self.headers['x-b3-flags'],
                'b3'               : self.headers['b3']
            }
            result = requests.get(coordinates_url, headers=headers)
            data = json.loads(result.text)

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