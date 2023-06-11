# Pip imports
from fastapi import FastAPI

# Standard library
import sqlite3
from sqlite3 import Error

db_file = "pythonsqlite.db"

def create_connection(db_file):
    '''
    Create a connection to the sqlite database.

    :params: db_file (str): Sqlite database file
    :returns: Sqlite database connection object, or None
    '''
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(f"Unable to create connection to sqlite database: {e}")
    finally:
        return conn
    
def create_users_table(conn):
    '''
    Create the users table.

    :params: conn (Sqlite Connection Object): Sqlite connection object
    :returns: True if successful, False otherwise
    '''
    create_users_command = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        password text NOT NULL,
                                        level text NOT NULL,
                                        category text NOT NULL,
                                        token text DEFAULT NULL
                                    ); """
    
    try:
        c = conn.cursor()
        c.execute(create_users_command)
    except Error as e:
        print(f"Unable to create users table: {e}")
        return False
    return True
    
def insert_users(conn):
    '''
    Insert users into table.

    :params: conn (Sqlite Connection Object): Sqlite connection object
    :returns: True if successful, False otherwise
    '''
    users = [
        {'username': 'alice.smith', 'password': '34563456', 'level': 's0', 'category': 'c1'},
        {'username': 'bob.hart', 'password': '34563456', 'level': 's0', 'category': 'c2'},
        {'username': 'katie.lowe', 'password': '34563456', 'level': 's0', 'category': 'c3'},
        {'username': 'sam.kent', 'password': '34563456', 'level': 's1', 'category': 'c4'},
        {'username': 'lora.garcia', 'password': '34563456', 'level': 's1', 'category': 'c5'},
        {'username': 'daniel.strasser', 'password': '34563456', 'level': 's1', 'category': 'c6'},
    ]

    for user in users:
        insert_users_command = f""" INSERT INTO users (username, password, level, category) 
                                    VALUES ('{user['username']}', '{user['password']}', '{user['level']}', '{user['category']}');"""
        try:
            c = conn.cursor()
            c.execute(insert_users_command)
        except Error as e:
            print(f"Unable to insert user into table: {e}")
            return False
    return True

def select_users(conn):
    '''
    Select all users from table.

    :params: conn (Sqlite Connection Object): Sqlite connection object
    :returns: Sqlite cursor object, or None
    '''
    select_users_command = """SELECT * FROM users;"""
    try:
        c = conn.cursor()
        users = c.execute(select_users_command)
    except Error as e:
        print(f"Unable to select users: {e}")
        return None 
    return users

def initalize_database(db_file):
    # Intialize the database and tables, if they don't already exist
    conn = create_connection(db_file)
    if not conn:
        exit(1)

    users_table_created = create_users_table(conn)
    if not users_table_created:
        exit(1)

    users_inserted = insert_users(conn)
    if not users_inserted:
        exit(1)
    
    users = select_users(conn)
    for user in users.fetchall():
        print(user)


app = FastAPI()

@app.on_event("startup")
async def startup():
    initalize_database(db_file)

@app.get("/")
async def root():
    return {"message": "Hello World"}