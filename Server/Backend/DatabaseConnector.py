import sqlite3
import logging
import os

LOG = logging.getLogger(__name__)

class DatabaseType:
    sqlite3 = "sqlite3"

class SQLite3DatabaseConnector:
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

    def insert(self, command, parameters = ()) -> bool:
        if not self.dbConnection:
            return False
        
        cursor = self.dbConnection.cursor()
        cursor.execute(command, parameters)
        self.dbConnection.commit()
        return True

    def delete(self, command):
        if not self.dbConnection:
            return False
        
        try:
            cursor = self.dbConnection.cursor()
            cursor.execute(command)
            self.dbConnection.commit()
        except Exception as e:
            LOG.exception("delete attempt finish with exception: {}".format(e))
            return False
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
        " RegistrationDate TEXT,",
        " Name TEXT,",
        " Login TEXT,",
        " Password TEXT,",
        " Email TEXT"
    ]
    DB.execute("CREATE TABLE USERS({})".format("".join(usersTable)))

    reservationsTable = [
        " ReservationId TEXT,",
        " ParkingSlotId TEXT,",
        " Login TEXT,",
        " ReservationDate TEXT,",
        " ReservationMadeDateTime TEXT"
    ]
    DB.execute("CREATE TABLE RESERVATIONS({})".format("".join(reservationsTable)))

    parkingslotsTable = [
        " ParkingSlotId TEXT,",
        " SlotNumber TEXT,",
        " Floor TEXT,",
        " PositionX INTEGER,",
        " PositionY INTEGER"
    ]
    DB.execute("CREATE TABLE PARKINGSLOTS({})".format("".join(parkingslotsTable)))
