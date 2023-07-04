from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class SimpleAPIHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type='text/plain'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self._set_response()
            response = 'Hello, World!'
            self.wfile.write(response.encode())
        elif self.path == '/my_function':
            self._set_response()
            result = my_function()
            response = f'The result of my_function is: {result}'
            self.wfile.write(response.encode())
        else:
            self._set_response(status_code=404)
            response = '404 Not Found'
            self.wfile.write(response.encode())

    def do_POST(self):
        if self.path == '/my_function':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            if 'param1' in data and 'param2' in data:
                self._set_response()
                result = my_function(data['param1'], data['param2'])
                response = f'The result of my_function is: {result}'
                self.wfile.write(response.encode())
            else:
                self._set_response(status_code=400)
                response = 'Bad Request: Missing parameters'
                self.wfile.write(response.encode())
        else:
            self._set_response(status_code=404)
            response = '404 Not Found'
            self.wfile.write(response.encode())


# we can access this function using end point http://localhost:8000/my_function

def my_function(param1=2, param2=5):
    # Your custom function logic goes here
    return param1 + param2


def run_server():
    host = 'localhost'
    port = 8000

    server = HTTPServer((host, port), SimpleAPIHandler)
    print(f'Starting server on {host}:{port}...')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print('Server stopped.')


if __name__ == '__main__':
    run_server()


# http://localhost:8000/