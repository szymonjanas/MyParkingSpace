import logging 
from DatabaseConnector import SQLite3DatabaseConnector
from utils import toTuple, toNamesFixture, toDbValuesFixture

LOG = logging.getLogger(__name__)

connector : SQLite3DatabaseConnector = None

def init_database_connector(dbConnector : SQLite3DatabaseConnector):
    global connector
    connector = dbConnector

class SqlTableName:
    USERS = "USERS"
    PARKINGSLOTS = "PARKINGSLOTS"

###############
###  WHERE  ###
###############

class SqlConditionConcatenator:
    AND = "AND"
    OR = "OR"

class SqlWhereCondition:
    def __init__(self, conditions):
        self.conditions = conditions

class SqlWhereBuilder:
    def __init__(self):
        self.conditionList = list()

    def addCondition(self, condition : dict, concatenator = SqlConditionConcatenator.AND):
        if len(condition.keys()) > 1:
            self.addConditions(condition, concatenator)
        for key, value in condition.items():
            if len(self.conditionList) > 1:
                self.conditionList.append(concatenator)
            self.conditionList.append("{}='{}'".format(key, value))
        return self

    def get(self) -> SqlWhereCondition:
        return SqlWhereCondition(' '.join(self.conditionList))

##############
### INSERT ###
##############

class InsertQuery:
    def __init__(self, 
                 query,
                 values):
        self.query = query
        self.values = values

class SqlInsertQueryExecutor:
    def __init__(self, insertQuery : InsertQuery):
        self.insertQuery = insertQuery

    def execute(self, dbConnector : SQLite3DatabaseConnector):
        LOG.debug("new insert request: {}".format(self.insertQuery.__dict__))
        return dbConnector.insert(self.insertQuery.query, self.insertQuery.values)

class SqlInsertQuery:
    def __init__(self, tableName : str):
        self.tableName = tableName

    def insert(self, model):
        return SqlInsertQueryExecutor(
                    InsertQuery(
                        query='INSERT INTO {table}({names}) VALUES({values})'.format(
                                table=self.tableName,
                                names=toNamesFixture(model),
                                values=toDbValuesFixture(model)), 
                        values=toTuple(model)))

##############
### SELECT ###
##############

class SelectQuery:
    def __init__(self, query):
        self.query = query

class SqlSelectQueryExecutor:
    def __init__(self,
                 selectQuery : SelectQuery):
        self.selectQuery = selectQuery

    def where(self, sqlWhereCondition : SqlWhereCondition):
        self.selectQuery.query += ' WHERE {}'.format(sqlWhereCondition.conditions)
        return self

    def execute(self, dbConnector : SQLite3DatabaseConnector):
        LOG.debug("new select request: {}".format(self.selectQuery.__dict__))
        return dbConnector.select(self.selectQuery.query).fetchall()

class SqlSelectQuery:
    def __init__(self, tableName : str):
        self.tableName = tableName

    def select(self, fixture : tuple):
        return SqlSelectQueryExecutor(
                    SelectQuery('SELECT {fixture} FROM {table}'.format(
                                    fixture=', '.join(fixture),
                                    table=self.tableName)))

##############
### DELETE ###
##############

class DeleteQuery:
    def __init__(self,
                 query):
        self.query = query

class SqlDeleteQueryExecutor:
    def __init__(self,
                 deleteQuery : DeleteQuery):
        self.deleteQuery = deleteQuery

    def where(self, sqlWhereCondition : SqlWhereCondition):
        self.deleteQuery.query += ' WHERE {}'.format(sqlWhereCondition.conditions)
        return self
    
    def execute(self, dbConnector : SQLite3DatabaseConnector):
        LOG.debug("new delete request: {}".format(self.deleteQuery.__dict__))
        return dbConnector.select(self.deleteQuery.query)

class SqlDeleteQuery:
    def __init__(self, tableName : str):
        self.tableName = tableName

    def delete(self):
        return SqlDeleteQueryExecutor(
                    DeleteQuery('DELETE FROM {}'.format(self.tableName)))
    
