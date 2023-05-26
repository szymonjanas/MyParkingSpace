import logging

def loadConfig():
    LOGGING_FORMAT = '[%(asctime)s] %(levelname)s/%(name)s: %(message)s'
    logging.basicConfig(
        format=LOGGING_FORMAT,
        handlers=[
            logging.FileHandler("../logs/backend.log"),
            logging.StreamHandler()
        ],
        level=logging.DEBUG)
