from main import *
from database.db_connector import *
from database.sqlite_queries import *

import datetime
import re

def init_setup():

    while 1:
        firstname = input("Enter your first name: ")
        lastname = input("Enter your last name: ")

        if firstname != "" and  lastname != "" and " " not in firstname and " " not in lastname:
            break
        else:
            print("Please give a valid first and last name, whitespace is not allowed")
            speak("Please give a valid first and last name, whitespace is not allowed")
            

    while 1:
        username = input("Choose your user name: ")
        
        if " " in username:
            print("No space allowed")
            speak("No space allowed")
        else:
            break

    while 1:
        gender = input("Enter your gender: ")
        gender_status = gender_validation(gender)
        if gender_status != False:
            break
    
    while 1:
        dob = input("Enter your date-of-birth: ")
        dob_status = validate_date(dob)
        if dob_status != False:
            break

    while 1:
        gmail_id = input("Enter your gmail.com id: ")
        email_status = validate_email(gmail_id)
        if email_status != False:
            break
        
    gmail_id = str(gmail_id)
    dob = str(dob)    
            
    speak("Please wait while we save your data safely")        
    print("Please wait while we save your data safely")

    db_status, init_db_name = first_time_save_to_database()

    if db_status == True:
        init_table_name = "init_info_table"

        #creating 1st table to store user info and init setup status
        init_create_table_status = create_table(init_table_name, init_db_name)
        print("init_create_table_status: ", init_create_table_status, "\n")
        
        #inserting info
        
        init_insert_status = insert_query(db_status, firstname, lastname, username, gender, dob, gmail_id, init_table_name, init_db_name)
        print("init_insert_status: ", init_insert_status, "\n")

        # select * , printing out the values
        select_status = select_query(init_table_name, init_db_name)

    return db_status

    # if db_status == True and init_create_table_status == True and init_insert_status == True and select_status == True: 

    #     return db_status
    # else:
    #     db_status = False
    #     return db_status  


    
def first_time_save_to_database():

    fail_counter = 0
    init_status = False
    db_name = "database\\db\\initial_db.db"

    while 1:
        database_name, status = create_database(db_name)
        if status == True:
            init_status = True
            break
        else:
            if fail_counter >= 5:
                speak('Could not store data, will try again later')
                print('Could not store data, will try again later')

                break
            else:
                fail_counter +=1
    
    return init_status, db_name


def validate_date(dob):

    status = True
    try:
        datetime.datetime.strptime(dob, '%Y-%m-%d')
        
    except ValueError:
        status = False
        print("Incorrect data format, should be YYYY-MM-DD")
        speak("Incorrect data format, should be YYYY-MM-DD")
        
    return status


def validate_email(email):
    email_regex = '^[\w.+\-]+@gmail\.com$' #'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'  <-- just email
    status = True

    if(re.search(email_regex, email)):  
        status = True  
          
    else:
        print("Incorrect email format, should be example@gmail.com or example.e@gmail.com")
        speak("Incorrect email format, should be example@gmail.com or example.e@gmail.com")
        status = False

    return status    

def gender_validation(gender):

    g_values = ['male', 'female', 'm', 'f']
    gender = gender.lower()
    status = True

    if gender not in g_values:
        print("Gender can only be male or female")
        speak("Gender can only be male or female")
        status = False
    else:
        status = True
        
    return status



#init_setup()