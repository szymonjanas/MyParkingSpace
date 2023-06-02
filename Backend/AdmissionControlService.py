from flask import Blueprint, request, Response, abort
import logging
import json
from datetime import datetime
import Database
from  models.users import User

api_admissionControlService = Blueprint("Admission Control Service", __name__)

LOG = logging.getLogger(__name__)

@api_admissionControlService.route("/register", methods = ['POST'])
def register():
    LOG.info("{}".format(request.method))

    registerData = request.json
    print(request.json)
    if not ("login" in registerData and 
            "password" in registerData and 
            "email" in registerData and
            "name" in registerData):
        abort(400)

    dbRows = Database.get_database().get_user_by_login(registerData["login"])
    print(dbRows)

    nowTime = datetime.now()
    todayDate = nowTime.strftime("%d.%m.%Y")
    user = User(
        1,
        todayDate,
        registerData["name"],
        registerData["login"],
        registerData["password"],
        registerData["email"]
    )
    Database.get_database().insert_user(user)

    # TODO add email validation
    # TODO add password encryption

    return "register route"
