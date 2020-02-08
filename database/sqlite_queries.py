import sqlite3

from  ui_and_stuff import colours

def create_table(table_name = "default", database_name = None):

    status = False
    conn = sqlite3.connect(database_name)
    try:
        conn.execute('''CREATE TABLE {}
                (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
                INIT_STATUS           TEXT    NOT NULL,
                FIRSTNAME           TEXT    NOT NULL,
                LASTNAME           TEXT    NOT NULL,
                USERNAME           TEXT    NOT NULL,
                GENDER           TEXT    NOT NULL,
                DOB           TEXT    NOT NULL,
                GMAIL_ID           TEXT    NOT NULL);'''.format(table_name))

        print ("Table {} created successfully".format(table_name))
        status = True
        conn.close()
    except Exception as e:
        colours.prRed("Error creating table in {}\n{}".format(table_name, )).reset_colour_style()
        # colours.reset_colour_style()
        print("Error creating table in {}\n{}".format(table_name, ))

    return status

def insert_query(INIT_STATUS, FIRSTNAME, LASTNAME, USERNAME, GENDER, DOB, GMAIL_ID, table_name = "default", database_name = None):

    status = False
    conn = sqlite3.connect(database_name)
    #print("\nIn Insert: {}, {}, {}, {}, {}, {}, {}, {}\n".format(table_name, INIT_STATUS, FIRSTNAME, LASTNAME, USERNAME, GENDER, DOB, GMAIL_ID))
    try:
        conn.execute("INSERT INTO {} (INIT_STATUS, FIRSTNAME, LASTNAME, USERNAME, GENDER, DOB, GMAIL_ID) \
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(table_name, INIT_STATUS, FIRSTNAME, LASTNAME, USERNAME, GENDER, DOB, GMAIL_ID));
        conn.commit()

        print ("Records created successfully in table {}".format(table_name))
        status = True
        conn.close()
    except Exception as e:
        colours.prRed("Error inserting query in table {}\n{}".format(table_name, e)).reset_colour_style()
        # colours.reset_colour_style()
        print("Error inserting query in table {}\n{}".format(table_name, e))

    return status

def select_query(table_name = "default", database_name = None):

    status = False
    conn = sqlite3.connect(database_name)
    try:
        cursor = conn.execute("SELECT * from {}".format(table_name))
        
        for row in cursor:
            print("ID = ", row[0])
            print("INIT_STATUS = ", row[1])
            INIT_STATUS = row[1]
            print("FIRSTNAME = ", row[2])
            print("LASTNAME = ", row[3])
            print("USERNAME = ", row[4])
            print("GENDER = ", row[5])
            print("DOB = ", row[6])
            print("GMAIL ID = ", row[7], "\n")

        status = True
        #print("Operation done successfully")
        conn.close()

        print("Inside select_query, INIT_STATUS: {}, INIT_STATUS type: {}".format(INIT_STATUS, type(INIT_STATUS)))
        return status, INIT_STATUS
    except Exception as e:
        colours.prRed("Error fetching data from table {}\n{}".format(table_name, e)).reset_colour_style()
        # colours.reset_colour_style()
        print("Error fetching data from table {}\n{}".format(table_name, e))

        return status    


def update_query(table_name = "default", database_name = None):

    status = False
    conn = sqlite3.connect(database_name)
    try:
        conn.execute("UPDATE {} set SALARY = 25000.00 where ID = 1".format(table_name))
        conn.commit()

        status = True
        print ("Total number of rows updated {} in table {}".format(conn.total_changes, table_name))
    except:
        colours.prRed("Error updating data in table {}".format(table_name)).reset_colour_style()
        # colours.reset_colour_style()
        print("Error updating data in table {}".format(table_name))

    return status    


def delete_query(table_name = "default", database_name = None):

    status = False
    conn = sqlite3.connect(database_name)
    try:    
        conn.execute("DELETE from {} where ID = 2;".format(table_name))
        conn.commit()
        status = True
        print ("Total number of rows deleted {} in table {}".format(conn.total_changes, table_name))
    except:
        colours.prRed("Error deleting data from table {}".format(table_name)).reset_colour_style()
        # colours.reset_colour_style()
        print("Error deleting data from table {}".format(table_name))    

    return status