import sys, json, os
import logging
import loggingConfig
import DatabaseConnector as dbService
from flask import Flask
import ConnectionTestService

configs = None
with open("Backend/config.json") as configFile:
    configs = json.load(configFile)
    configFile.close()

hostApi = Flask("MyParkingSpaceServer")
hostApi.register_blueprint(ConnectionTestService.api_connectionTestService)

def RUN_APPLICATION(hostIpAddress, port, logFilePath):
    if not logFilePath:
        logFilePath = configs["defaults"]["logsFilePath"]
    if os.path.exists(logFilePath):
        os.remove(logFilePath)
    loggingConfig.loadConfig(logFilePath)
    LOG = logging.getLogger(__name__)
    LOG.info('Hello world!')
    LOG.info("Log file location: {}".format(logFilePath))
    database = dbService.DatabaseService()
    database.connect(configs["defaults"]["sqliteDatabasePath"]) # TODO add database path option from argv

    if not hostIpAddress:
        hostIpAddress = "127.0.0.1"
    LOG.info("Flask IP Address: {}:{}".format(hostIpAddress, port))
    hostApi.run(
        host = hostIpAddress,
        port = port
    )

    database.disconnect()

if __name__ == "__main__":

    ipAddress = None
    logFilePath = None
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--ipaddress":
            ipAddress = sys.argv[i+1]
            i+=1
        if sys.argv[i] == "--logfilepath":
            logFilePath = sys.argv[i+1]
            i+=1

    # TODO przyjmowanie komend na ip i nazwę log file
    RUN_APPLICATION(ipAddress, "5566", logFilePath)
