import logging
import loggingConfig

loggingConfig.loadConfig()

LOG = logging.getLogger(__name__)


if __name__ == "__main__":
    LOG.info('Hello world!')
