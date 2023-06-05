import sys
import logging
import DatabaseConnector as dbService
import Database
from flask import Flask
from services import ConnectionTest, AdmissionControl, SpaceReservation
import config
from utils import SupportedArgs, ArgvDeserializer, ApplicationConfig
import utils

class Application:
    ipAddress = None
    port = None

    def __init__(self, appConfig : ApplicationConfig):
        self.setLoggingConfig(appConfig.logFilePath, appConfig.logLevel)
        
        self.LOG.info('Hello world!')

        self.initDatabase(appConfig.databasePath, appConfig.newDatabase)

        self.setIpAddress(appConfig.ipAddress)
        self.setPort(appConfig.port)

        self.initServer()

    def __del__(self):
        if self.database:
            self.database.disconnect()

    def setLoggingConfig(self, logsFilePath, logLevel):
        if not logsFilePath:
            logsFilePath = config.LOGS_FILE_PATH_DEFAULT

        self.LOG = logging.getLogger(__name__)
        self.LOG.info("Log file location: {}".format(logsFilePath))
        
        if not logLevel:
            logLevel = config.LOG_LEVEL_DEFAULT

        if not logsFilePath:
            self.LOG.warn("Log file path does not exist!")
            logging.basicConfig(
                format=config.LOGGING_FORMAT,
                handlers=[
                    logging.StreamHandler()
                ],
                level=logLevel)
            return

        with open(logsFilePath, "w") as file:
            pass
    
        logging.basicConfig(
            format=config.LOGGING_FORMAT,
            handlers=[
                logging.FileHandler(logsFilePath),
                logging.StreamHandler()
            ],
            level=logLevel)
                

    def initDatabase(self, databasePath, newDatabase : bool = None):
        self.database = dbService.DatabaseConnector()
        if not databasePath:
            databasePath = config.SQLITE_DATABASE_PATH_DEFAULT
        dbService.generateNewDatabase(databasePath, newDatabase)
        self.database.connect(databasePath) # TODO add database path option from argv
        Database.init_database(Database.DatabaseFacade(self.database))

    def setIpAddress(self, ipAddress : str = None):
        self.ipAddress = ipAddress
        if not self.ipAddress:
            self.ipAddress = config.IP_ADDRESS

    def setPort(self, port : str = None):
        self.port = port
        if not port:
            self.port = config.PORT

    def initServer(self):
        self.flaskServer = Flask(config.SERVER_NAME)
        self.flaskServer.register_blueprint(ConnectionTest.api_connectionTestService)
        self.flaskServer.register_blueprint(AdmissionControl.api_admissionControlService)
        self.flaskServer.register_blueprint(SpaceReservation.api_spaceReservation)

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

    args = ArgvDeserializer(sys.argv)

    app = Application(
        ApplicationConfig(
            ipAddress = args.GetArg(SupportedArgs.ipaddress),
            logFilePath = args.GetArg(SupportedArgs.logfilepath),
            databasePath = args.GetArg(SupportedArgs.databasepath),
            logLevel = utils.convertLogLevel(args.GetArg(SupportedArgs.loglevel)),
            newDatabase = args.GetArg(SupportedArgs.newdatabase)
        )
    )
    app.runServer()
