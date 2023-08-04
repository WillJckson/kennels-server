import sqlite3
from models import Employee
from models import Location
EMPLOYEES = [
    {
    "id": 1,
    "name": "Jenna Solis",
    "locationId": 1
    },
    {
    "name": "Emma Beaton",
    "address": "54 Sycamore Avenue",
    "locationId": 2
    }
]

def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.name location_name,
            l.address location_address
        FROM Employee e
        JOIN Location l
            ON l.id = e.location_id;
        """)

        # Initialize an empty list to hold all employee representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
        # Create a employee instance from the current row.
        # Note that the database fields are specified in
        # exact order of the parameters defined in the
        # employee class above.
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])

            location = Location(row['location_id'], row['location_name'], row['location_address'])

            employee.location = location.__dict__

            employees.append(employee.__dict__)

    return employees

def create_employee(employee):
    # Get the id value of the last employee in the list
    max_id = EMPLOYEES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the employee dictionary
    employee["id"] = new_id

    # Add the employee dictionary to the list
    EMPLOYEES.append(employee)

    # Return the dictionary with `id` property added
    return employee

# Function with a single parameter
def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an employee instance from the current row
        employee = Employee(data['id'], data['name'], data['address'], data['location_id'])

        return employee.__dict__

def get_employee_by_location(location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.location_id = ?
        """, (location,))
        # Fetch all the matching rows from the query result
        rows = db_cursor.fetchall()
        # Process the rows and return the data, for example, as a list of dictionaries
        employees = []
        for row in rows:
            employee = {
                'id': row['id'],
                'name': row['name'],
                'address': row['address'],
                'location_id': row['location_id'],
            }
            employees.append(employee)

        return employees