from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse, mimetypes, pathlib, socket, threading, datetime, json
from server import run_server
from client import run_client



class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('./index.html')
        elif pr_url.path == './message':
            self.send_html_file('./message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        print(filename)
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())
    
    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        print(self.path)
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        print(data)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server = ('127.0.0.1', 5000)
            sock.connect(server)
            sock.sendto(data, server)
    
        finally:
            if sock:
                sock.close()
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()

def run(UDP_IP, server_class=HTTPServer, handler_class=HttpHandler):
    server_address = (UDP_IP, 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


UDP_IP = '127.0.0.1'
UDP_PORT = 3000

SERVER_UDP = 5000

if __name__ == '__main__':
    http_server = threading.Thread(target=run, args=(UDP_IP,))
    server = threading.Thread(target=run_server, args=(UDP_IP, SERVER_UDP))
    client = threading.Thread(target=run_client, args=(UDP_IP, SERVER_UDP))
    http_server.start()
    server.start()
    client.start()
    

    http_server.join()
    server.join()
    client.join()
    
    print('Done!')