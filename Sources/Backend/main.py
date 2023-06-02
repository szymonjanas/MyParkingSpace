import logging
import loggingConfig
loggingConfig.loadConfig()
import DatabaseService as dbService


LOG = logging.getLogger(__name__)


if __name__ == "__main__":
    LOG.info('Hello world!')
    database = dbService.DatabaseService()
    database.connect("../database/backend.db")

