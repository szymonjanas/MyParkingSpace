import logging
import Testing.SystemTestConsts as consts
import sqlite3
import os

class System:
    linux : str = "linux"
    windows : str = "windows"
    ci_linux : str = "ci_linux"

class SystemTestContext:
    system = System.windows
    loglevel : int = logging.INFO
    logFilePath : str = consts.LOGS_FILE_PATH
    databasePath : str = consts.DATABASE_TEST_PATH
    logDirectoryPath : str = consts.LOG_DIRECTORY_PATH

    def __init__(self):
        self.clearLogFile()
        self.initLogging()
        self.LOG = logging.getLogger()

    def initLogging(self):
        logging.basicConfig(
            format='[%(asctime)s] %(message)s',
            handlers=[
                logging.FileHandler(self.logFilePath),
                logging.StreamHandler()
            ],
            level=self.loglevel)

    def setSystem(self, system = None):
        if system:
            self.system = system
        self.LOG.debug("SystemTest is running on: {}".format(self.system))
    
    def getSystem(self):
        return self.system

    def setLogLevel(self, loglevel):
        self.loglevel = loglevel
        self.LOG.setLevel(loglevel)
        self.LOG.info("SystemTest logging level set as {}".format(loglevel))

    def IsDebug(self):
        return self.loglevel == logging.DEBUG

    def getPythonRunCommand(self):
        if self.system == System.linux:
            return "python3"
        elif self.system == System.windows:
            return "py"
        elif self.system == System.ci_linux:
            return "python"
    
    def clearLogFile(self):
        with open(self.logFilePath, "w") as file:
            pass

    def setDatabasePath(self, dbPath):
        self.databasePath = dbPath

    def clearDatabaseTable(self, table : str):
        databaseConnector = sqlite3.connect(self.databasePath)
        dbCursor = databaseConnector.cursor()
        dbCursor.execute("DELETE FROM {}".format(table))
        databaseConnector.commit()

    def clearTestsLogsDirectory(self):
        files = os.listdir(self.logDirectoryPath)
        for file in files:
            if file.endswith(".log"):
                file_path = os.path.join(self.logDirectoryPath, file)
                os.remove(file_path)
    