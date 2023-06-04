from DatabaseConnector import DatabaseConnector
from  models.users import User
import logging 

LOG = logging.getLogger(__name__)

class DatabaseFacade:
    databaseConnector : DatabaseConnector

    def __init__(self, dbConnector):
        self.databaseConnector = dbConnector

    def select_all_users_details(self, details):
        cmd = 'SELECT {} FROM USERS'.format(details)
        LOG.debug("select all users details: " + cmd)
        out = self.databaseConnector.select(cmd).fetchall()
        return out
    
    def select_user_details_where(self, details, where):
        cmd = 'SELECT {} FROM USERS WHERE {}'.format(details, where)
        LOG.debug("select user details where: " + cmd)
        out = self.databaseConnector.select(cmd).fetchall()
        return out

    def insert_user(self, user : User):
        cmd = 'INSERT INTO USERS({}) VALUES({})'.format(user.toNamesFixture(), user.dbValues())
        LOG.debug("new user insert: {}".format(cmd))
        return self.databaseConnector.insert(cmd, user.toTuple())
    
    def select_parking_slots(self):
        cmd = 'SELECT * FROM PARKINGSLOTS'
        LOG.debug("select parkning slots: {}".format(cmd))
        return self.databaseConnector.select(cmd).fetchall()

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
