import DatabaseConnector
import sqlite3
from  models.users import User

class DatabaseFacade:
    databaseConnector : DatabaseConnector.DatabaseConnector

    def __init__(self, dbConnector):
        self.databaseConnector = dbConnector

    def get_user_by_login(self, login):
        return self.databaseConnector.select('SELECT Name, Login, Email FROM USERS'.format(login)).fetchall()
    
    def insert_user(self, user : User):
        self.databaseConnector.insert('INSERT INTO USERS({}) VALUES(?,?,?,?,?,?)'.format(user.toNamesFixture()), user.toTuple())

__DatabaseFacade__ : DatabaseFacade = None

def is_database():
    global __DatabaseFacade__
    return bool(__DatabaseFacade__)

def get_database():
    global __DatabaseFacade__
    return __DatabaseFacade__

def init_database(dbFacade : DatabaseFacade):
    global __DatabaseFacade__
    __DatabaseFacade__ = dbFacade
