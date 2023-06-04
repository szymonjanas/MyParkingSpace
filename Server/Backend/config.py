import json, logging

__configs__ = None


def getFromConfig(category, variable):
    global __configs__
    if not __configs__:
        with open("Backend/config.json") as configFile:
            __configs__ = json.load(configFile)
            configFile.close()
    if category in __configs__.keys():
        if variable in __configs__[category]:
            return __configs__[category][variable]
    return None

SQLITE_DATABASE_PATH_DEFAULT = getFromConfig("defaults","sqliteDatabasePath")

LOGS_FILE_PATH_DEFAULT = getFromConfig("defaults", "logsFilePath")

LOGGING_FORMAT = '[%(asctime)s] %(levelname)s/%(name)s: %(message)s'

SERVER_NAME = "MyParkingSpaceServer"

IP_ADDRESS = getFromConfig("defaults", "ipAddress")
PORT  = getFromConfig("defaults", "port")

LOG_LEVEL_DEFAULT = logging.INFO
