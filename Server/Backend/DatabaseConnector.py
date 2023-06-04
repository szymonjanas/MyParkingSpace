import sqlite3
import logging
import os

LOG = logging.getLogger(__name__)

class DatabaseConnector:
    dbConnection = None

    def __init__(self):
        LOG.info("Database version: {}".format(sqlite3.version))

    def connect(self, dbFileName):
        LOG.debug("Connecting database to: {}".format(dbFileName))
        try:
            self.dbConnection = sqlite3.connect(dbFileName, check_same_thread=False)
            LOG.info("Database connected: {}".format(dbFileName))
        except Exception as err:
            LOG.exception(err)
            self.disconnect()
 
    def disconnect(self):
        if self.dbConnection:
            self.dbConnection.close()
            self.dbConnection = None
            LOG.info("Database connection closed!")

    def select(self, command, parameters = ()):
        if not self.dbConnection:
            return
        
        cursor = self.dbConnection.cursor()
        return cursor.execute(command, parameters)

    def insert(self, command, parameters = ()):
        if not self.dbConnection:
            return False
        
        cursor = self.dbConnection.cursor()
        cursor.execute(command, parameters)
        self.dbConnection.commit()
        return True


def generateNewDatabase(databasePath, removeIfExist : bool = False):
    LOG.warn("Creating new database: {}, with flag removeIfExist as {}".format(databasePath, removeIfExist))
    if os.path.exists(databasePath) and removeIfExist:
        os.remove(databasePath)
    else:
        return

    databaseConnector = sqlite3.connect(databasePath)
    DB = databaseConnector.cursor()

    usersTable = [
        " UserProfileId INTEGER,",
        " RegistrationDate TEXT,",
        " Name TEXT,",
        " Login TEXT,",
        " Password TEXT,",
        " Email"
    ]
    DB.execute("CREATE TABLE USERS({})".format("".join(usersTable)))

    reservationsTable = [
        " ReservationId TEXT,",
        " UserProfileId INTEGER,",
        " ReservationDate TEXT,",
        " ReservationTimeStart TEXT,",
        " ReservationTimeEnd TEXT,",
        " ReservationMadeDate TEXT,",
        " ReservationMadeTime TEXT"
    ]
    DB.execute("CREATE TABLE RESERVATIONS({})".format("".join(reservationsTable)))

    parkingslotsTable = [
        " SlotNumber INTEGER,",
        " ReservationId TEXT,",
        " PositionX INTEGER,",
        " PositionY INTEGER"
    ]
    DB.execute("CREATE TABLE PARKINGSLOTS({})".format("".join(parkingslotsTable)))


    # FIXME DUMB GENERATION OF RANDOM DATA - has to be moved to tests module
    DB.execute('INSERT INTO PARKINGSLOTS( "SlotNumber", "ReservationId" ) VALUES ( "1", "X2")')
    databaseConnector.commit()
    DB.execute('INSERT INTO PARKINGSLOTS( "SlotNumber", "ReservationId" ) VALUES ( "2", "X3")')
    databaseConnector.commit()
    DB.execute('INSERT INTO PARKINGSLOTS( "SlotNumber", "ReservationId" ) VALUES ( "3", "X4")')
    databaseConnector.commit()
    DB.execute('INSERT INTO PARKINGSLOTS( "SlotNumber", "ReservationId" ) VALUES ( "4", "X5")')
    databaseConnector.commit()
    DB.execute('INSERT INTO PARKINGSLOTS( "SlotNumber", "ReservationId" ) VALUES ( "5", "X6")')
    databaseConnector.commit()