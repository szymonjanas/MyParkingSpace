import sqlite3
import sys, os

databasePath = "Backend/database/backend.sqlite"
for i in range(1, len(sys.argv)):
    if sys.argv[i] == "--path":
        databasePath = sys.argv[i+1]

if os.path.exists(databasePath):
    doRemove = input("Remove existing database? Y/N: ")
    if doRemove.upper() == "Y" or doRemove.upper() == "YES":
        os.remove(databasePath)
    else:
        print("Database exist, remove it first or change name for new database!")
        quit()

databaseConnector = sqlite3.connect(databasePath)
DB = databaseConnector.cursor()

usersTable = [
    " UserProfileId INTEGER,",
    " RegistrationDate TEXT,",
    " Username TEXT,",
    " Login TEXT,",
    " Password TEXT,",
    " Email"
]
DB.execute("CREATE TABLE USERS({})".format("".join(usersTable)))

reservationsTable = [
    " ReservationId INTEGER,",
    " UserProfileId INTEGER,",
    " ReservationDate TEXT,",
    " ReservationTimeStart TEXT,",
    " ReservationTimeEnd TEXT,",
    " ReservationMadeDate TEXT,",
    " ReservationMadeTime TEXT"
]

DB.execute("CREATE TABLE RESERVATIONS({})".format("".join(reservationsTable)))


