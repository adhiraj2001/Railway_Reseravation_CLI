import subprocess as sp
import pymysql
import pymysql.cursors
from tabulate import tabulate

# import os

# from dotenv import load_dotenv
# load_dotenv()

# MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
# MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
# DB_NAME = os.getenv("DB_NAME")
# MYSQL_HOST = os.getenv("MYSQL_HOST")

# connection = pymysql.connect(host=MYSQL_HOST,
#                              user=MYSQL_USERNAME, password=MYSQL_PASSWORD, db=DB_NAME,
#                              cursorclass=pymysql.cursors.DictCursor)


def hireAnEmployee():
    """
    This is a sample function implemented for the refrence.
    This example is related to the Employee Database.
    In addition to taking input, you are required to handle domain errors as well
    For example: the SSN should be only 9 characters long
    Sex should be only M or F
    If you choose to take Super_SSN, you need to make sure the foreign key constraint is satisfied
    HINT: Instead of handling all these errors yourself, you can make use of except clause to print the error returned to you by MySQL
    """
    try:
        # Takes emplyee details as input
        row = {}
        print("Enter new employee's details: ")
        name = (input("Name (Fname Minit Lname): ")).split(' ')
        row["Fname"] = name[0]
        row["Minit"] = name[1]
        row["Lname"] = name[2]
        row["Ssn"] = input("SSN: ")
        row["Bdate"] = input("Birth Date (YYYY-MM-DD): ")
        row["Address"] = input("Address: ")
        row["Sex"] = input("Sex: ")
        row["Salary"] = float(input("Salary: "))
        row["Dno"] = int(input("Dno: "))

        query = "INSERT INTO EMPLOYEE(Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Dno) VALUES('%s', '%c', '%s', '%s', '%s', '%s', '%c', %f, %d)" % (
            row["Fname"], row["Minit"], row["Lname"], row["Ssn"], row["Bdate"], row["Address"], row["Sex"], row["Salary"], row["Dno"])

        print(query)
        cur.execute(query)
        connection.commit()

        print("Inserted Into Database")

    except Exception as e:
        connection.rollback()
        print("Failed to insert into database")
        print(">>>>>>>>>>>>>", e)

    return

def find_trains():

    print('List of all stations with their station_ids: ')
    query = """SELECT * from station;"""
    cur.execute(query)
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()
    
    source = input("Enter your source station_id: ")
    destination = input("Enter your destination station_id: ")

    print('Available Trains with {} to {} in their route: '.format(source, destination))
    query = """SELECT * from train_status
            WHERE train_id IN (SELECT (A.train_id) FROM train as A
                WHERE (A.starts_at = %s AND (A.ends_at = %s OR %s IN (SELECT B.station_id FROM route AS B WHERE B.train_id = A.train_id)))
                OR (A.ends_at = %s AND %s in (SELECT B.station_id FROM route WHERE B.train_id = A.train_id))
                OR ((SELECT (B.stop_no) FROM route AS B WHERE B.train_id = A.train_id AND B.station_id = %s) < ANY (SELECT (C.stop_no) FROM route AS C WHERE C.train_id = A.train_id AND C.station_id = %s)));"""
    
    cur.execute(query, (source, destination, destination, destination, source, source, destination))
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()

    return res


def dispatch(user_id):
    while True:

        print("1. Book a ticket")  # Hire an Employee
        print("2. Find trains from source to destination.")
        print("3. Find your booked tickets")  # Fire an Employee
        print("4. Exit")
        print()

        choice = int(input("Enter choice> "))
        print()

        if choice == 1:
            display_user()
        elif choice == 2:
            select_user()
        elif choice == 3:
            create_user()
        elif choice == 4:
            exit(0)
        else:
            print('Incorrent choice.')
        print()



def display_user():
    print('All users_ids:')

    query = """SELECT * from user;"""
    cur.execute(query)
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()

def select_user():

    user_id = int(input('Enter user_id: '))
    password = input('Enter password: ')
    print()

    query = """SELECT * from user WHERE user_id=%s AND password=%s;"""
    cur.execute(query, (user_id, password))
    # connection.commit()

    res = cur.fetchall()

    if(len(res) == 0):
        print('Incorrect user_id or password.')
        print()
        return

    print('Logged in Successfully.')
    print()
        
    dispatch(user_id)

def create_user():
    
    password = input('Set Password for New User: ')
    print()
    
    try:
        query = """INSERT INTO user (password) VALUES(%s);"""
        cur.execute(query, (password))
        connection.commit()

    except Exception as e:
        connection.rollback()

        print("Failed to insert into database")
        print(">>>>>>>>>>>>>", e)
        print()
        return
    
    print('Logged in Successfully.')
    print()

    query = """SELECT COUNT(user_id) from user;"""
    cur.execute(query)

    res = cur.fetchall()

    dispatch(res[0]['COUNT(user_id)'])



if __name__ == "__main__":

    try:
        connection = pymysql.connect(host='localhost', user='root', 
                            password='pwd', port=30306, db='railway', cursorclass=pymysql.cursors.DictCursor)
        
        sp.call('clear', shell=True)

        if connection.open:
            print('Successfully Connected to the Database')
            print()
        else:
            print('Failed to connect')
            print()
            exit(0)

    except Exception as e:
        sp.call('clear', shell=True)
        print(e)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        print()


    while True:

        try:
            # using cursor
            with connection.cursor() as cur:
                    
                print("1. Display all User_id")  # Hire an Employee
                print("2. Select a User_id")
                print("3. Create new User_id")  # Fire an Employee
                print("4. Exit")
                print()

                choice = int(input("Enter choice> "))
                print()

                if choice == 1:
                    display_user()
                elif choice == 2:
                    select_user()
                elif choice == 3:
                    create_user()
                elif choice == 4:
                    exit(0)
                else:
                    print('Incorrent choice.')
                print()

        except Exception as e:
            # sp.call('clear', shell=True)
            print(e)
            print()
