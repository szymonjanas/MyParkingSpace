from flask import Blueprint, send_from_directory
import os

api_reactConnector = Blueprint("React Connector Service", __name__)

STATIC_FOLDER = '../frontend/build'

@api_reactConnector.route('/', defaults={'path': ''})
@api_reactConnector.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(STATIC_FOLDER + '/' + path):
        return send_from_directory(STATIC_FOLDER, path)
    else:
        return send_from_directory(STATIC_FOLDER, 'index.html')