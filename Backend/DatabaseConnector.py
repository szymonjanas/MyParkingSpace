import sqlite3
import logging

LOG = logging.getLogger(__name__)

class DatabaseConnector:
    dbConnection = None

    def __init__(self):
        LOG.info("Database version: {}".format(sqlite3.version))

    def connect(self, dbFileName):
        LOG.debug("Connecting database to: {}".format(dbFileName))
        try:
            self.dbConnection = sqlite3.connect(dbFileName)
            LOG.info("Database connected: {}".format(dbFileName))
        except Exception as err:
            LOG.exception(err)
            self.disconnect()
 
    def disconnect(self):
        if self.dbConnection:
            self.dbConnection.close()
            self.dbConnection = None
            LOG.info("Database connection closed!")

    def execute(self, command):
        if not self.dbConnection:
            return
        
        cursor = self.dbConnection.cursor()
        return cursor.execute(command)
