from DatabaseConnector import DatabaseConnector
from  models.users import User
import logging 

LOG = logging.getLogger(__name__)

class DatabaseFacade:
    databaseConnector : DatabaseConnector

    def __init__(self, dbConnector):
        self.databaseConnector = dbConnector

    def get_all_users_details(self, details):
        cmd = 'SELECT {} FROM USERS'.format(details)
        LOG.debug("command: " + cmd)
        out = self.databaseConnector.select(cmd).fetchall()
        LOG.debug("output: {}".format(out))
        return out
    
    def insert_user(self, user : User):
        cmd = 'INSERT INTO USERS({}) VALUES({})'.format(user.toNamesFixture(), user.dbValues())
        LOG.debug("new insert cmd: {}".format(cmd))
        return self.databaseConnector.insert(cmd, user.toTuple())

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
