import psycopg2


def create_table(conn):
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Clients(
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    surname VARCHAR(20) NOT NULL,
    email VARCHAR(40) NOT NULL);''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Numbers(
    id SERIAL PRIMARY KEY,
    id_client INTEGER REFERENCES Clients(id),
    number VARCHAR(12));''')
    conn.commit()
    cur.close()


def add_clients(conn, name, surname, email):
    cur = conn.cursor()
    cur.execute('''INSERT INTO Clients(name, surname, email) VALUES(%s, %s, %s);''',
                (name, surname, email))
    conn.commit()
    cur.close()


def add_numbers(conn, id_client, number):
    cur = conn.cursor()
    cur.execute('''INSERT INTO Numbers(id_client, number) VALUES(%s, %s);''',
                (id_client, number))
    conn.commit()
    cur.close()


def update_client(conn, client_id, name=None, surname=None, email=None):
    cur = conn.cursor()
    cur.execute('''UPDATE Clients SET name=%s, surname=%s, email=%s WHERE id=%s''',
                (name, surname, email, client_id))
    conn.commit()
    cur.close()


def delete_number(conn, client_id, number):
    cur = conn.cursor()
    cur.execute('''DELETE FROM Numbers WHERE id_client=%s AND number=%s''',
                (client_id, number))
    conn.commit()
    cur.close()


def delete_client(conn, client_id):
    cur = conn.cursor()
    cur.execute('''DELETE FROM Clients WHERE id=%s''',
                (client_id,))
    conn.commit()
    cur.close()


def find_client(conn, name=None, surname=None, email=None, number=None):
    cur = conn.cursor()
    if name is None and surname is None and number is None:
        cur.execute('''SELECT c.*, n.number FROM Clients AS c
        LEFT JOIN Numbers AS n ON n.id_client = c.id  
        WHERE email=%s''', (email,))
        print('fetchall', cur.fetchall())
        cur.close()
    elif surname is None and email is None and number is None:
        cur.execute('''SELECT c.*, n.number FROM Clients AS c
         LEFT JOIN Numbers AS n ON n.id_client = c.id 
         WHERE name=%s''', (name,))
        print('fetchall', cur.fetchall())
        cur.close()
    elif name is None and email is None and number is None:
        cur.execute('''SELECT c.*, n.number FROM Clients AS c
        LEFT JOIN Numbers AS n ON n.id_client = c.id  
        WHERE surname=%s''', (surname,))
        print('fetchall', cur.fetchall())
        cur.close()
    elif name is None and surname is None and email is None:
        cur.execute('''SELECT c.*, n.number FROM Clients AS c
        LEFT JOIN Numbers AS n ON n.id_client = c.id  
        WHERE n.number=%s''', (number,))
        print('fetchall', cur.fetchall())
        cur.close()


with psycopg2.connect(database='employees', user='postgres', password='0509') as conn:
