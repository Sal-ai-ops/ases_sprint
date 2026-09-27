from http.server import HTTPServer, BaseHTTPRequestHandler

class SinkHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        print(f"\n[SINK INTERCEPTED DATA]: {body}\n")
        self.send_response(200)
        self.end_headers()

print("Egress Sink listening on port 8080...")
HTTPServer(('0.0.0.0', 8080), SinkHandler).serve_forever()
