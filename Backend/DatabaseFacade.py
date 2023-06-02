import DatabaseConnector
import sqlite3


class DatabaseFacade:
    databaseConnector : DatabaseConnector.DatabaseConnector

    def __init__(self, dbConnector):
        self.databaseConnector = dbConnector


__DatabaseFacade__ = None

def is_database():
    global __DatabaseFacade__
    return bool(__DatabaseFacade__)

def get_database():
    global __DatabaseFacade__
    return __DatabaseFacade__

def init_database(dbFacade : DatabaseFacade):
    global __DatabaseFacade__
    __DatabaseFacade__ = dbFacade
