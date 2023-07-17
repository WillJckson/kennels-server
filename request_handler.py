import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import (get_all_animals, get_single_animal, create_animal, delete_animal, update_animal,
get_single_employee, get_all_employees, create_employee,get_single_customer, get_all_customers, create_customer, get_single_location, get_all_locations, create_location)


class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        try:
            id = int(path_params[2])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id)

    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            if id is not None:
                response = get_single_animal(id)
            else:
                response = get_all_animals()
        elif resource == "employees":
            if id is not None:
                response = get_single_employee(id)
            else:
                response = get_all_employees()
        elif resource == "customer":
            if id is not None:
                response = get_single_customer(id)
            else:
                response = get_all_customers()
        elif resource == "locations":
            if id is not None:
                response = get_single_location(id)
            else:
                response = get_all_locations()

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource) = self.parse_url(self.path)

    # Initialize new resource variables
        new_resource = None

        if resource == "employees":
            new_resource = create_employee(post_body)
        if resource == "animals":
            new_resource = create_animal(post_body)
        if resource == "customers":
            new_resource = create_customer(post_body)
        if resource == "locations":
            new_resource = create_location(post_body)

        self.wfile.write(json.dumps(new_resource).encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())
        
    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            update_animal(id, post_body)

    # Encode the new animal and send in response
        self.wfile.write("".encode())
    
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()


def main():
    host = ''
    port = 8088
    server = HTTPServer((host, port), HandleRequests)
    server.serve_forever()


if __name__ == "__main__":
    main()
