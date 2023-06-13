from flask import Blueprint, send_from_directory
import os
import logging

api_reactConnector = Blueprint("React Connector Service", __name__)

STATIC_FOLDER = '../frontend/build'

LOG = logging.getLogger(__name__)

@api_reactConnector.route('/', defaults={'path': ''})
@api_reactConnector.route('/<path:path>')
def serve(path):
    LOG.debug("Attempt to get react files!")
    if path != "" and os.path.exists(STATIC_FOLDER + '/' + path):
        return send_from_directory(STATIC_FOLDER, path)
    else:
        return send_from_directory(STATIC_FOLDER, 'index.html')
