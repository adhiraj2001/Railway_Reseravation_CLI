<!-- # Railway Reservation CLI -->
<!-- A CLI to give a simulate online Railway Reservation system, interface written in Python with data stored in a MySQL DB. Final project for the Data and Applications Course, Monsoon 2021. -->

# Data and Application Project

> **Team Name**: RNA

> **Team Members**: Adhiraj Deshmukh (2021121012), Pranjal Thapliyal (2020101108), Sukhjinder Kumar (2020101055)

> **Project Video Link**: [DnA Project Video](https://drive.google.com/file/d/15drWtoazWEFKiJPkea9AmQf0Jy9b2XYU/view?usp=sharing)

## Running the Project

### Initialize Database

First we would need to initialize the database, to do that we need to run the
`CREATE_TABLES.sql` script from the *SQL* folder. 
To run the script enter this command in your MySQL Shell:

```bash
source SQL/CREATE_TABLES.sql
```

If this doesn't work directly copy pasting the whole contents of the file directly onto the shell works too.

### Setting up PyMySql variable values 

Change the `.env` file and replace all the environment variable values with the required values. 
There are 4 values in this file:

1. `MYSQL_USERNAME` → username for MySQL
2. `MYSQL_PASSWORD` → password for MySQL
3. `DB_NAME` → The name of the database populated with `CREATE_TABLES.sql`.
4. `MYSQL_HOST` → The hostname of MySQL server.

`port:30306` is not going to change since this is the version of MySQL we have tested our code with.

> **Alternative**: You can just edit the code and write all the information related to PyMySql directly. This would be preferable since it takes less time and is easier therefore we have commented out the part from the code which makes uses `.env` variables.

### Dependencies Required in this Project

To install the required python libraries:

```bash
python3 -m pip install PyMySql
python3 -m pip install tabulate
python3 -m pip install python-dotenv
```
### Execute File

To run the python file:

```bash
python3 Python/CLI.py
```

## Commands Supported:

### Login Stage

- `Display all user_id` : Initially for logging into a user, this command displays all the user_ids (and their passwords :)) to help with the login stage
- `Select user_id` : Login to existing user_id
- `Create user_id` : Create new user_id and set password
- `Delete user_id` : Delete user_id, only if you know it's password, would also delete all data related to the user (like booked ticket) from thee database
- `Exit` : Exit from the code

### User Stage

- `Book ticket` : Book a ticket according to source and destination and available trains, using login user_id
- `Update Ticket Status` : Command to Update your booked tickets status, which means confirms which tickets are confirmed according to available seats
- `View train schedule` : Just displays whole train schedule
- `Find trains source to destination` : Displays trains that go from given source and destination
- `Find total cost` : Total cost for the user depending on the tickets booked on which trains
- `Add passenger` : Add passenger information
- `Update passenger` : Update passenger information
- `Delete passenger` : Delete passenger, would also delete booked tickets related to the passenger
- `Search Train` : Prefix search trains
- `Search Station` : Search search stations
- `Log Out` : Log out from current user