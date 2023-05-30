import logging

def loadConfig(logsFilePath):
    LOGGING_FORMAT = '[%(asctime)s] %(levelname)s/%(name)s: %(message)s'
    logging.basicConfig(
        format=LOGGING_FORMAT,
        handlers=[
            logging.FileHandler(logsFilePath),
            logging.StreamHandler()
        ],
        level=logging.DEBUG)
