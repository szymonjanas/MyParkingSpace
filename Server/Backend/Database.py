from DatabaseConnector import DatabaseConnector
from  models.users import User
from models.parkingslot import ParkingSlot
import logging 
from utils import toTuple, toNamesFixture, toDbValuesFixture

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
    
    def select_user_details_where(self, details : list, where : dict):
        details = ', '.join(details)
        whereStr = str()
        idx = 0
        for key, value in where.items():
            whereStr += "{}='{}'".format(key, value)
            if idx < len(where.keys())-1:
                whereStr += " AND "
            idx += 1
        cmd = 'SELECT {} FROM USERS WHERE {}'.format(details, whereStr)
        LOG.debug("select user details where: " + cmd)
        out = self.databaseConnector.select(cmd).fetchall()
        return out

    def insert_user(self, user : User):
        cmd = 'INSERT INTO USERS({}) VALUES({})'.format(
            toNamesFixture(user), toDbValuesFixture(user)
        )
        LOG.debug("new user insert: {}".format(cmd))
        return self.databaseConnector.insert(cmd, toTuple(user))
    
    def insert_parking_slot(self, slot : ParkingSlot):
        cmd = 'INSERT INTO PARKINGSLOTS({}) VALUES({})'.format(
            toNamesFixture(slot), toDbValuesFixture(slot)
        )
        LOG.debug("new parking slot: {}".format(slot.__dict__))
        return self.databaseConnector.insert(cmd, toTuple(slot))

    def select_parking_slots(self):
        cmd = 'SELECT * FROM PARKINGSLOTS'
        LOG.debug("select parking slots: {}".format(cmd))
        return self.databaseConnector.select(cmd).fetchall()
    
    def clear_all_parking_slots(self):
        cmd = "DELETE FROM PARKINGSLOTS"
        LOG.debug("delete all parking slots: {}".format(cmd))
        return self.databaseConnector.delete(cmd)

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
