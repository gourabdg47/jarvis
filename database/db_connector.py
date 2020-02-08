import sqlite3

def create_database(database_name):

    status = False
    try:
        conn = sqlite3.connect(database_name)
        status = True
        print ("Created database successfully\n")
    except:
        print ("Error creating database\n")

    return database_name, status

