import subprocess as sp
import pymysql
import pymysql.cursors
from tabulate import tabulate
import time

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

try:
    connection = pymysql.connect(host='localhost', user='root', 
                        password='pwd', port=30306, db='railway', cursorclass=pymysql.cursors.DictCursor)
    
    sp.call('clear', shell=True)

    if connection.open:
        print('> Successfully Connected to the Database')
        print()
    else:
        print('> Failed to connect')
        print()
        exit(0)

except Exception as e:
    sp.call('clear', shell=True)

    print(e)
    print("> Connection Refused: Either username or password is incorrect or user doesn't have access to database")
    print()


### global update variable:
user_no = 0
passenger_no = 0
ticket_no = 0


def book(cur, user_id):
    global ticket_no

    print('List of all passengers with their passenger_ids: ')
    query = """SELECT passenger_id, name from passenger;"""
    cur.execute(query)
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()
    
    passenger_id = int(input("Enter passenger_id: "))
    print()

    sp.call('clear', shell=True)

    flag = 0
    for x in res:
        if x['passenger_id'] == passenger_id:
            flag = 1
            break

    if flag == 0:
        print('> Error: passenger_id not found.')
        print()
        return

    print('List of all stations with their station_ids: ')
    query = """SELECT * from station;"""
    cur.execute(query)
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()
    
    source = int(input("Enter your source station_id: "))
    destination = int(input("Enter your destination station_id: "))
    print()

    sp.call('clear', shell=True)

    flag1 = 0
    flag2 = 0
    for x in res:
        if x['station_id'] == source:
            flag1 = 1

        if x['station_id'] == destination:
            flag2 = 1

    if flag1 == 0:
        print("> Error: source '{}' station_id not found.".format(source))
        print()
        return

    if flag2 == 0:
        print("> Error: destination '{}' station_id not found.".format(destination))
        print()
        return

    # finding all trains that go through source and destination
    res = find_trains(cur, source, destination)
    
    if len(res) == 0:
        print("> No Trains found from '{}' to '{}' station_ids.".format(source, destination))
        print()
        return

    train_id = int(input('Train_id to book: '))
    date = input("Date of booking (YYYY-MM-DD): ")
    print()

    sp.call('clear', shell=True)

    flag = 0
    for x in res:
        if x['train_id'] == train_id and x['date'].strftime('%Y-%m-%d') == date:
            flag = 1
            break

    if flag == 0:
        print("> Train id '{}' on date '{}' for your source '{}' and destination '{}' not found.".format(train_id, date, source, destination))
        # print(type(res[0]['train_id']), type(train_id), type(res[0]['date']), type(date))
        print()
        return 

    try:
        query = """INSERT INTO ticket (ticket_id, date, source, destination) VALUES(%s, %s, %s, %s);"""
        cur.execute(query, (ticket_no + 1, date, source, destination))
        connection.commit()

    except Exception as e:
        connection.rollback()

        print("Failed to insert into database")
        print(">>>>>>>>>>>>>", e)
        print()
        return
    
    ticket_no += 1

    try:
        query = """INSERT INTO books VALUES(%s, %s, %s, %s, %s);"""
        cur.execute(query, (user_id, passenger_id, ticket_no, train_id, date))
        connection.commit()

    except Exception as e:
        connection.rollback()

        print("> Failed to insert into database")
        print(">>>>>>>>>>>>>", e)
        print()
        return

    print('> Ticket Booked.')
    print()


def trains_find(cur):

    print('List of all stations with their station_ids: ')
    query = """SELECT * from station;"""
    cur.execute(query)
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()
    
    source = int(input("Enter your source station_id: "))
    destination = int(input("Enter your destination station_id: "))
    print()

    sp.call('clear', shell=True)

    flag1 = 0
    flag2 = 0
    for x in res:
        if x['station_id'] == source:
            flag1 = 1

        if x['station_id'] == destination:
            flag2 = 1

    if flag1 == 0:
        print("> Error: source '{}' station_id not found.".format(source))
        print()
        return

    if flag2 == 0:
        print("> Error: destination '{}' station_id not found.".format(destination))
        print()
        return

    # finding all trains that go through source and destination
    res = find_trains(cur, source, destination)

    if len(res) == 0:
        print("> No Trains found for source '{}' and destination '{}'".format(source, destination))
        print()


def find_trains(cur, source, destination):

    print('Available Train schedule with {} to {} in their route: '.format(source, destination))
    query = """SELECT P.train_id, Q.name, P.date from train_status AS P INNER JOIN train AS Q ON P.train_id = Q.train_id
            WHERE P.train_id IN (SELECT A.train_id FROM train as A
                WHERE (A.starts_at = %s AND (A.ends_at = %s OR %s IN (SELECT B.station_id FROM route AS B WHERE B.train_id = A.train_id)))
                OR (A.ends_at = %s AND %s in (SELECT C.station_id FROM route as C WHERE C.train_id = A.train_id))
                OR ((SELECT D.stop_no FROM route AS D WHERE D.train_id = A.train_id AND D.station_id = %s) < ANY (SELECT E.stop_no FROM route AS E WHERE E.train_id = A.train_id AND E.station_id = %s)));"""
    
    cur.execute(query, (source, destination, destination, destination, source, source, destination))
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()

    return res


def user_tickets(cur, user_id):
    print('Booked Tickets: ')

    query = """SELECT user_id, ticket_id, train_id, date FROM books
            WHERE user_id = %s;"""

    cur.execute(query, (user_id))
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()


def train_schedule(cur):
    print('All trains schedule:')

    query = """SELECT A.train_id, B.name, A.date FROM train_status AS A INNER JOIN train AS B ON A.train_id = B.train_id;"""
    cur.execute(query)
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()


def total_cost(cur, user_id):
    print('All tickets total cost for user:')

    query = """SELECT A.user_id, SUM(B.price) AS total_cost FROM
            (SELECT user_id, train_id FROM books WHERE user_id = %s) AS A
            INNER JOIN
            (SELECT train_id, price FROM train) AS B
            ON A.train_id = B.train_id
            GROUP BY A.user_id;"""

    cur.execute(query, (user_id))
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()


def add_passenger(cur):
    global passenger_no

    name = input("Enter passenger name: ")
    dob = input("Enter dob (YYYY-MM-DD): ")
    gender = input("Gender: ")
    print()

    sp.call('clear', shell=True)


    try:
        query = """INSERT INTO passenger (passenger_id, name, dob, gender)
        VALUES(%s, %s, %s, %s);"""
        
        cur.execute(query, (passenger_no + 1, name, dob, gender))
        connection.commit()

    except Exception as e:
        connection.rollback()

        print("> Failed to insert into database")
        print(">>>>>>>>>>>>>", e)
        print()
        return

    passenger_no += 1

    print('> Passenger table inserted.')
    print()


    mobile = int(input("Enter new mobile number: "))
    print()

    sp.call('clear', shell=True)

    if mobile == 0:
        return

    try:
        query = """INSERT INTO passenger_contact VALUES(%s, %s);"""
        
        cur.execute(query, (passenger_no, mobile))
        connection.commit()

    except Exception as e:
        connection.rollback()

        print("> Failed to insert into database")
        print(">>>>>>>>>>>>>", e)
        print()
        return

    print('> Passenger_contact table inserted.')
    print()


    street = input("Enter street address: ")
    city = input("Enter city: ")
    state = input("Emter state: ")
    print()

    sp.call('clear', shell=True)

    if len(street) == 0 and len(city) == 0 and len(state) == 0:
        return

    try:
        query = """INSERT INTO passenger_address VALUES(%s, %s, %s, %s);"""
        
        cur.execute(query, (passenger_no, street, city, state))
        connection.commit()

    except Exception as e:
        connection.rollback()

        print("> Failed to insert into database")
        print(">>>>>>>>>>>>>", e)
        print()
        return

    print('> Passenger_address table inserted.')
    print()


def update_passenger(cur):
    
    print('List of all passengers with their passenger_ids: ')
    query = """SELECT passenger_id, name from passenger;"""
    cur.execute(query)
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()
    
    passenger_id = int(input("Enter passenger_id: "))
    print()

    sp.call('clear', shell=True)

    flag = 0
    for x in res:
        if x['passenger_id'] == passenger_id:
            flag = 1
            break

    if flag == 0:
        print('> Error: passenger_id not found.')
        print()
        return
    
    print("1. Update Name")
    print("2. Add new mobile no.")
    print("3. Add new address")
    print()

    choice = int(input("Enter choice> "))
    print()

    sp.call('clear', shell=True)

    if choice == 1:

        name = input("Enter updated name: ")
        print()

        sp.call('clear', shell=True)

        if len(name) == 0:
            return

        try:
            query = """UPDATE passenger SET name = %s
            WHERE passenger_id = %s;"""
            
            cur.execute(query, (name, passenger_id))
            connection.commit()

        except Exception as e:
            connection.rollback()

            print("> Failed to insert into database")
            print(">>>>>>>>>>>>>", e)
            print()
            return

        print('> Passenger Table updated.')
        print()

    elif choice == 2:

        mobile = int(input("Enter new mobile number: "))
        print()

        sp.call('clear', shell=True)

        if mobile == 0:
            return

        try:
            query = """INSERT INTO passenger_contanct
            VALUES(%s, %s);"""
            
            cur.execute(query, (passenger_id, mobile))
            connection.commit()

        except Exception as e:
            connection.rollback()

            print("> Failed to insert into database")
            print(">>>>>>>>>>>>>", e)
            print()
            return

        print('> Passenger_contact table inserted.')
        print()

    elif choice == 3:

        street = input("Enter street address: ")
        city = input("Enter city: ")
        state = input("Emter state: ")
        print()

        sp.call('clear', shell=True)

        if len(street) == 0 and len(city) == 0 and len(state) == 0:
            return

        try:
            query = """INSERT INTO passenger_address
            VALUES(%s, %s, %s, %s);"""
            
            cur.execute(query, (passenger_id, street, city, state))
            connection.commit()

        except Exception as e:
            connection.rollback()

            print("> Failed to insert into database")
            print(">>>>>>>>>>>>>", e)
            print()
            return

        print('> Passenger_address table inserted.')
        print()

    
def delete_passenger(cur):
    
    print('List of all passengers with their passenger_ids for passenger: ')
    query = """SELECT passenger_id, name FROM passenger;"""

    cur.execute(query)
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()
    
    passenger_id = int(input("Enter passenger_id: "))
    print()

    sp.call('clear', shell=True)

    flag = 0
    for x in res:
        if x['passenger_id'] == passenger_id:
            flag = 1
            break

    if flag == 0:
        print('> Error: passenger_id did not match.')
        print()
        return

    try:
        query = """DELETE FROM passenger
                WHERE passenger_id = %s;"""
        
        cur.execute(query, (passenger_id))
        connection.commit()

    except Exception as e:
        connection.rollback()

        print("> Failed to delete from passenger")
        print(">>>>>>>>>>>>>", e)
        print()
        return

    print('passenger table row deleted')
    print()


def update_ticket_status(cur, user_id):

    try:
        query = """UPDATE ticket SET status = 1
                WHERE ticket_id IN 
                (SELECT ticket_id FROM books AS B WHERE user_id = %s AND 
                ((SELECT booked_seats FROM train_status AS C WHERE C.train_id = B.train_id AND C.date = B.date) <= (SELECT total_seats FROM train AS D WHERE D.train_id = B.train_id)));"""
        
        cur.execute(query, (user_id))
        connection.commit()

    except Exception as e:
        connection.rollback()

        print("> Failed to update into database")
        print(">>>>>>>>>>>>>", e)
        print()
        return

    print('> Ticket Table updated.')
    print()

    print('List of all tickets with their status: ')
    query = """SELECT A.ticket_id, A.date, B.status FROM
            (SELECT ticket_id, date FROM books WHERE user_id = %s) AS A
            INNER JOIN
            (SELECT ticket_id, date, status FROM ticket) AS B
            ON A.ticket_id = B.ticket_id AND A.date = B.date;"""
    cur.execute(query, (user_id))
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()


def delete_ticket(cur, user_id):

    print('List of all tickets with their ticket_ids for user: ')
    query = """SELECT B.user_id, A.ticket_id FROM
            (SELECT ticket_id FROM ticket) AS A
            INNER JOIN
            (SELECT user_id, ticket_id FROM books WHERE user_id = %s) AS B
            ON A.ticket_id = B.ticket_id;"""

    cur.execute(query, (user_id))
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()
    
    ticket_id = int(input("Enter ticket_id: "))
    print()

    sp.call('clear', shell=True)

    flag = 0
    for x in res:
        if x['ticket_id'] == ticket_id:
            flag = 1
            break

    if flag == 0:
        print('> Error: ticket_id not found.')
        print()
        return

    try:
        query = """DELETE FROM ticket
                WHERE ticket_id = %s;"""
        
        cur.execute(query, (ticket_id))
        connection.commit()

    except Exception as e:
        connection.rollback()

        print("> Failed to delete from ticket.")
        print(">>>>>>>>>>>>>", e)
        print()
        return

    print('> ticket table row deleted')
    print()


def search_train(cur):

    name = input("Enter train name (prefix): ")
    print()

    sp.call('clear', shell=True)

    name = name + "%"

    query = """SELECT name, train_id from train WHERE name like %s"""

    cur.execute(query, (name))
    # connection.commit()

    res = cur.fetchall()

    print("Train names matching with '{}': ".format(name))

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()


def search_station(cur):

    name = input("Enter station name (prefix): ")
    print()

    sp.call('clear', shell=True)

    name = name + "%"

    query = """SELECT name, station_id from station WHERE name like %s"""

    cur.execute(query, (name))
    # connection.commit()

    res = cur.fetchall()

    print("Station names matching with '{}': ".format(name))

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()


def dispatch(cur, user_id):
    while True:
        print("1. Book a ticket")
        print("2. Update Ticket Status")
        print("3. Delete Ticket")
        print("4. View all Train schedule")
        print("5. Find Train schedules which travel from source to destination")
        print("6. Find your booked tickets")
        print("7. Find total cost for user")
        print("8. Add passenger")
        print("9. Update passenger")
        print("10. Delete passenger")
        print("11. Search Trains by Names similarity")
        print("12. Search Stations by Names similarity")
        print("13. Log Out")
        print()

        choice = int(input("Enter choice> "))
        print()

        sp.call('clear', shell=True)

        if choice == 1:
            book(cur, user_id)
        elif choice == 2:
            update_ticket_status(cur, user_id)
        elif choice == 3:
            delete_ticket(cur, user_id)
        elif choice == 4:
            train_schedule(cur)
        elif choice == 5:
            trains_find(cur)
        elif choice == 6:
            user_tickets(cur, user_id)
        elif choice == 7:
            total_cost(cur, user_id)
        elif choice == 8:
            add_passenger(cur)
        elif choice == 9:
            update_passenger(cur)
        elif choice == 10:
            delete_passenger(cur)
        elif choice == 11:
            search_train(cur)
        elif choice == 12:
            search_station(cur)
        elif choice == 13:
            print('> Logging Out.')
            print()
            break
        else:
            print('> Incorrent choice.')
        print()


def display_user(cur):
    print('All users_ids:')

    query = """SELECT * from user;"""
    cur.execute(query)
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()


def select_user(cur):

    user_id = int(input('Enter user_id: '))
    password = input('Enter password: ')
    print()

    sp.call('clear', shell=True)

    query = """SELECT * from user WHERE user_id=%s AND password=%s;"""
    cur.execute(query, (user_id, password))
    # connection.commit()

    res = cur.fetchall()

    if(len(res) == 0):
        print('> Incorrect user_id or password.')
        print()
        return

    print('> Logged in Successfully.')
    print()
        
    dispatch(cur, user_id)


def create_user(cur):
    global user_no
    
    password = input('> Set Password for New User: ')
    print()

    sp.call('clear', shell=True)
    
    try:
        query = """INSERT INTO user (user_id, password) VALUES(%s, %s);"""
        cur.execute(query, (user_no + 1, password))
        connection.commit()

    except Exception as e:
        connection.rollback()

        print("> Failed to insert into database")
        print(">>>>>>>>>>>>>", e)
        print()
        return

    user_no += 1
    
    print('> Logged in Successfully.')
    print()

    dispatch(cur, user_no)


def delete_user(cur):
    
    print('List of all users with their user_ids: ')
    query = """SELECT user_id FROM user;"""

    cur.execute(query)
    # connection.commit()

    res = cur.fetchall()

    print(tabulate(res, headers="keys", tablefmt='psql'))
    print()
    
    user_id = int(input("Enter user_id: "))
    password = input("Enter password: ")
    print()

    sp.call('clear', shell=True)


    query = """SELECT * FROM user;"""
    cur.execute(query)
    # connection.commit()

    res = cur.fetchall()

    flag = 0
    for x in res:
        if x['user_id'] == user_id and x['password'] == password:
            flag = 1
            break

    if flag == 0:
        print('> Error: user_id or password not match.')
        print()
        return

    try:
        query = """DELETE FROM user
                WHERE user_id = %s;"""
        
        cur.execute(query, (user_id))
        connection.commit()

    except Exception as e:
        connection.rollback()

        print("> Failed to delete from user")
        print(">>>>>>>>>>>>>", e)
        print()
        return

    print('> user table row deleted')
    print()


if __name__ == "__main__":

    while True:
        try:
            
            # using cursor
            with connection.cursor() as cur:

                if user_no == 0:
                    query = """SELECT MAX(user_id) from user;"""
                    cur.execute(query)
                    res = cur.fetchall()

                    user_no = res[0]['MAX(user_id)']

                if passenger_no == 0:
                    query = """SELECT MAX(passenger_id) from passenger;"""
                    cur.execute(query)
                    res = cur.fetchall()

                    passenger_no = res[0]['MAX(passenger_id)']
                
                if ticket_no == 0:
                    query = """SELECT MAX(ticket_id) from ticket;"""
                    cur.execute(query)
                    res = cur.fetchall()

                    ticket_no = res[0]['MAX(ticket_id)']

                print("1. Display all user_id")
                print("2. Select a user_id")
                print("3. Create new user_id")
                print("4. Delete user_id")
                print("5. Exit")
                print()

                choice = int(input("Enter choice> "))
                print()

                sp.call('clear', shell=True)

                if choice == 1:
                    display_user(cur)
                elif choice == 2:
                    select_user(cur)
                elif choice == 3:
                    create_user(cur)
                elif choice == 4:
                    delete_user(cur)
                elif choice == 5:
                    print('> Exiting Program.')
                    print()
                    exit(0)
                else:
                    print('> Incorrent choice.')
                print()

        except Exception as e:
            # sp.call('clear', shell=True)
            print(e)
            print()
