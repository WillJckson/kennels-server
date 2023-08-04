import sqlite3
from models import Animal
from models import Location
from models import Customer


def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address,
            c.name customer_name,
            c.address customer_address,
            c.password customer_password, 
            c.email customer_email
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        JOIN Customer c
            ON c.id = a.customer_id;
                """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            # Create an animal instance from the current row
            animal = Animal(row['id'], row['name'], row['breed'],row['status'], row['location_id'], row['customer_id'])
            location = Location(row['location_id'], row['location_name'], row['location_address'])
            customer = Customer(row['customer_id'], row['customer_name'],row['customer_address'], row['customer_email'], row['customer_password'])
            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__
            animal.customer = customer.__dict__
            # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)

    return animals


def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['breed'],
            new_animal['status'], new_animal['locationId'],
            new_animal['customerId'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id

    return new_animal


def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))

# Function with a single parameter


def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(data['id'], data['name'], data['breed'],
                        data['status'], data['location_id'],
                        data['customer_id'])

        return animal.__dict__


def get_animal_by_location(location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
        a.id,
        a.name,
        a.breed,
        a.status,
        a.location_id,
        a.customer_id
        from Animal a
        WHERE a.location_id = ?
        """, (location,))
        # Fetch all the matching rows from the query result
        rows = db_cursor.fetchall()
        # Process the rows and return the data, for example, as a list of dictionaries
        animals = []
        for row in rows:
            animal = {
                'id': row['id'],
                'name': row['name'],
                'breed': row['breed'],
                'status': row['status'],
                'location_id': row['location_id'],
                'customer_id': row['customer_id']
            }
            animals.append(animal)

        return animals


def get_animal_by_treatment(status):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
        a.id,
        a.name,
        a.breed,
        a.status,
        a.location_id,
        a.customer_id
        FROM Animal a
        WHERE a.status = ?
        """, (status,))  # Pass the 'status' parameter as a tuple here

        # Fetch all the matching rows from the query result
        rows = db_cursor.fetchall()

        # Process the rows and return the data, for example, as a list of dictionaries
        animals = []
        for row in rows:
            animal = {
                'id': row['id'],
                'name': row['name'],
                'breed': row['breed'],
                'status': row['status'],
                'customer_id': row['customer_id']
            }
            animals.append(animal)

        return animals
