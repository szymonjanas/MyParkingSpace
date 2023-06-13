from flask import Blueprint

api_connectionTestService = Blueprint("Connection Test Service", __name__)

@api_connectionTestService.route("/api/helloworld", methods = ['GET'])
def connectionTest():
    return "Hello World!"
