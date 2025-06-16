import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from smtp_client import send_email

CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "justin@cloudwranglers.io")
SERVER_PORT = int(os.getenv("CONTACT_PORT", 8081))

class ContactHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/contact":
            self.send_error(404, "Not Found")
            return
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        data = parse_qs(body)

        name = data.get('name', [''])[0]
        email = data.get('email', [''])[0]
        company = data.get('company', [''])[0]
        message = data.get('message', [''])[0]

        email_subject = f"Website contact from {name or 'Unknown'}"
        email_body = f"Name: {name}\nEmail: {email}\nCompany: {company}\n\n{message}"

        send_email(CONTACT_EMAIL, email_subject, email_body)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Thank you for your message.")


def run(server_class=HTTPServer, handler_class=ContactHandler):
    server = server_class(("", SERVER_PORT), handler_class)
    print(f"Listening on port {SERVER_PORT}...")
    server.serve_forever()


if __name__ == "__main__":
    run()
