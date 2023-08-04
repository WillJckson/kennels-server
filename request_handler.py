import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import (get_all_animals, get_single_animal, create_animal, delete_animal, update_animal, get_animal_by_location, get_animal_by_treatment,
get_customer_by_email, create_employee,get_single_customer, get_all_customers, create_customer, create_location, get_employee_by_location, get_all_employees, get_single_employee)
from urllib.parse import urlparse, parse_qs

class HandleRequests(BaseHTTPRequestHandler):
    # replace the parse_url function in the class
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)
                else:
                    response = get_all_animals()
            elif resource == "customers":
                if id is not None:
                    response = get_single_customer(id)
                else:
                    response = get_all_customers()
            elif resource == "employees":
                if id is not None:
                    response = get_single_employee(id)
                else:
                    response = get_all_employees()

        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed

            # see if the query dictionary has an email key
            if query.get('email') and resource == 'customers':
                response = get_customer_by_email(query['email'][0])
            elif query.get('location_id') and resource == 'animals':
                location_id = int(query['location_id'][0])
                response = get_animal_by_location(location_id)
            elif query.get('location_id') and resource == 'employees':
                location_id = int(query['location_id'][0])
                response = get_employee_by_location(location_id)
            elif query.get('status') and resource == 'animals':
                status = query['status'][0]
                response = get_animal_by_treatment(status)
                
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
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

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
