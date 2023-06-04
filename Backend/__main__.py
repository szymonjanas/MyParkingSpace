import sys, json, os
import logging
import DatabaseConnector as dbService
import Database
from flask import Flask
from services import ConnectionTest, AdmissionControl
import config
import utils

class Application:
    ipAddress = None
    port = None

    def __init__(self, ipAddress : str = None, port : str = None, logFilePath : str = None):
        self.setLoggingConfig(logFilePath)
        
        self.LOG.info('Hello world!')

        self.initDatabase()

        self.setIpAddress(ipAddress)
        self.setPort(port)

        self.initServer()

    def __del__(self):
        if self.database:
            self.database.disconnect()

    def setLoggingConfig(self, logsFilePath):
        if not logsFilePath:
            logsFilePath = config.LOGS_FILE_PATH_DEFAULT
        with open(logsFilePath, "w") as file:
            pass

        self.LOG = logging.getLogger(__name__)
        self.LOG.info("Log file location: {}".format(logsFilePath))

        logging.basicConfig(
            format=config.LOGGING_FORMAT,
            handlers=[
                logging.FileHandler(logsFilePath),
                logging.StreamHandler()
            ],
            level=logging.DEBUG)

    def initDatabase(self):
        self.database = dbService.DatabaseConnector()
        self.database.connect(config.SQLITE_DATABASE_PATH_DEFAULT) # TODO add database path option from argv
        Database.init_database(Database.DatabaseFacade(self.database))

    def setIpAddress(self, ipAddress : str = None):
        self.ipAddress = ipAddress
        if not self.ipAddress:
            self.ipAddress = "127.0.0.1"

    def setPort(self, port : str = None):
        self.port = port
        if not port:
            self.port = "5566"

    def initServer(self):
        self.flaskServer = Flask(config.SERVER_NAME)
        self.flaskServer.register_blueprint(ConnectionTest.api_connectionTestService)
        self.flaskServer.register_blueprint(AdmissionControl.api_admissionControlService)

    def runServer(self):
        if not self.ipAddress or not self.port:
            self.LOG.error("IpAddress or Port does not exist!")
            return

        if not self.flaskServer:
            self.LOG.error("Flask server has not been initiated!")
            return

        self.LOG.info("Flask Server run with address: {}:{}".format(self.ipAddress, self.port))

        self.flaskServer.run(
            host = self.ipAddress,
            port = self.port
        )

if __name__ == "__main__":

    args = utils.ArgvDeserializer(sys.argv)

    # TODO custom database path
    app = Application(
        ipAddress = args.GetArg(utils.SupportedArgs.ipaddress),
        logFilePath = args.GetArg(utils.SupportedArgs.logfilepath)
    )
    app.runServer()
