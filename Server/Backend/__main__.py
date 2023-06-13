import sys
import logging
import DatabaseConnector as dbService
import Database
from flask import Flask, send_from_directory
from services import ConnectionTest, AdmissionControl, SpaceReservation, ReactConnector
import config
from utils import SupportedArgs, ArgvDeserializer, ApplicationConfig
import utils
import EmailSender
from flask_cors import CORS

class Application:
    ipAddress = None
    port = None

    def __init__(self, appConfig : ApplicationConfig):
        self.setLoggingConfig(appConfig.logFilePath, appConfig.logLevel)
        
        self.LOG.info('Hello world!')

        self.setTestMode(appConfig.testMode)

        self.initDatabase(
            appConfig.databasePath,
            appConfig.newDatabase,
            appConfig.databaseType)

        self.initEmailSender(
            appConfig.emailConfig,
            appConfig.emailAddress,
            appConfig.emailPassword
        )

        self.setIpAddress(appConfig.ipAddress)
        self.setPort(appConfig.port)

        self.initServer()

    def __del__(self):
        if self.database:
            self.database.disconnect()

    def setTestMode(self, testMode):
        config.TEST_MODE = bool(testMode)

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
                

    def initDatabase(self, databasePath,
                           newDatabase : bool = None,
                           databaseType : str = None):
        if not databasePath:
            databasePath = config.SQLITE_DATABASE_PATH_DEFAULT

        if not databaseType or databaseType == dbService.DatabaseType.sqlite3:
            self.database = dbService.SQLite3DatabaseConnector()

            # FIXME I don't like that solution, but I don't have any better idea
            dbService.generateNewDatabase(databasePath, newDatabase)

        self.database.connect(databasePath) # TODO add database path option from argv
        Database.init_database_connector(self.database)

    def initEmailSender(self, emailConfig, emailaddress, password):
        if emailConfig:
            emailaddress = config.getFromConfig("email", "address")
            password = config.getFromConfig("email", "password")

        EmailSender.init_email_sender(
            address=emailaddress, password=password)

    def setIpAddress(self, ipAddress : str = None):
        self.ipAddress = ipAddress
        if not self.ipAddress:
            self.ipAddress = config.IP_ADDRESS

    def setPort(self, port : str = None):
        self.port = port
        if not port:
            self.port = config.PORT

    def initServer(self):
        self.flaskServer = Flask(config.SERVER_NAME, static_folder='../frontend/build')
        CORS(self.flaskServer)
        self.flaskServer.register_blueprint(ConnectionTest.api_connectionTestService)
        self.flaskServer.register_blueprint(AdmissionControl.api_admissionControlService)
        self.flaskServer.register_blueprint(SpaceReservation.api_spaceReservation)
        self.flaskServer.register_blueprint(ReactConnector.api_reactConnector)

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
            ipAddress =     args.GetArg(SupportedArgs.ipaddress),
            logFilePath =   args.GetArg(SupportedArgs.logfilepath),
            databasePath =  args.GetArg(SupportedArgs.databasepath),
            logLevel = utils.convertLogLevel(
                            args.GetArg(SupportedArgs.loglevel)),
            newDatabase =   args.GetArg(SupportedArgs.newdatabase),
            databasetype =  args.GetArg(SupportedArgs.databasetype),
            emailAddress =  args.GetArg(SupportedArgs.emailaddress),
            emailPassword = args.GetArg(SupportedArgs.emailpassword),
            emailConfig =   args.GetArg(SupportedArgs.emailconfig),
            testMode =      args.GetArg(SupportedArgs.testmode)
        )
    )
    app.runServer()
