import json

__configs__ = None
with open("Backend/config.json") as configFile:
    configs = json.load(configFile)
    configFile.close()

SQLITE_DATABASE_PATH_DEFAULT = configs["defaults"]["sqliteDatabasePath"]
LOGS_FILE_PATH_DEFAULT = configs["defaults"]["logsFilePath"]

LOGGING_FORMAT = '[%(asctime)s] %(levelname)s/%(name)s: %(message)s'

SERVER_NAME = "MyParkingSpaceServer"
