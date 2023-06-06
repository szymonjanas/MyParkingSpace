from flask import Blueprint, request, Response, abort
import logging
import json
from datetime import datetime
import Database as db
from  models.users import User
import utils
import authentication
from services import common
from utils import toTuple

api_admissionControlService = Blueprint("Admission Control Service", __name__)

LOG = logging.getLogger(__name__)

@api_admissionControlService.route("/register", methods = ['POST'])
def register():

    registerData = request.json
    requestId = utils.nextRequestId("reg_")
    LOG.info("Registration attempt [{}] with data: {}".format(requestId, request.json))
    if not ("login" in registerData and 
            "password" in registerData and 
            "email" in registerData and
            "name" in registerData):
        reason = "At least one registration parameter is invalid!"
        LOG.warn("Registration [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    if (len(registerData["login"]) == 0 or
        len(registerData["password"]) == 0 or 
        len(registerData["email"]) == 0 or
        len(registerData["name"]) == 0):
        reason = "At least one registration parameter is empty!"
        LOG.warn("Registration [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    dbRows = db.SqlSelectQuery(db.SqlTableName.USERS) \
                .select((User.Login, User.Email)) \
                .execute(db.connector)
    
    if len(dbRows) > 0:
        if len(list(filter(lambda item: item[0]==registerData["login"], dbRows))):
            reason = 'User with login {} is already registered!'.format(registerData["login"])
            LOG.warn("Registration [{}] aborted: {}".format(requestId, reason))
            abort(400, reason)
        if len(list(filter(lambda item: item[1]==registerData["email"], dbRows))):
            reason = 'User with email {} is already registered!'.format(registerData["email"])
            LOG.warn("Registration [{}] aborted: {}".format(requestId, reason))
            abort(400, reason)


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

    isSuccessfull = db.SqlInsertQuery(db.SqlTableName.USERS) \
                        .insert(user) \
                        .execute(db.connector)

    # TODO add email validation
    # TODO add password encryption

    if not isSuccessfull: # special corner case - not tested in system test
        reason = "Internal database connection issue!"
        LOG.error("Registration [{}] aborted: {}".format(requestId, reason))
        abort(500, reason)

    LOG.info("Registration [{}] successfull, new user details: {}".format(requestId, toTuple(user)))
    message = {'message': 'Successful registration!'}
    response = Response(json.dumps(message), status=201, mimetype='application/json')
    return response

@api_admissionControlService.route("/login", methods = ['POST'])
def login():
    loginData = request.json
    requestId = utils.nextRequestId("login_")
    LOG.info("Login attempt [{}] with data: {}".format(requestId, loginData))

    if not ("login" in loginData and 
            "password" in loginData):
        reason = "At least one login parameter is invalid!"
        LOG.warn("Login [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    if (len(loginData["login"]) == 0 or
        len(loginData["password"]) == 0):
        reason = "At least one login parameter is empty!"
        LOG.warn("Login [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    loginParam = loginData["login"]

    dbRows = db.SqlSelectQuery(db.SqlTableName.USERS) \
                    .select((User.Login, User.Password)) \
                    .where(db.SqlWhereBuilder() \
                            .addCondition({User.Login: loginParam}).get()) \
                    .execute(db.connector)
    if (len(dbRows) == 0):
        reason = "User with login {} is not registered!".format(loginParam)
        LOG.info("Login [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    password = dbRows[0][1]
    if not (password == loginData["password"]):
        reason = "Wrong password for user: {}!".format(loginParam)
        LOG.info("Login [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    token = authentication.generateSessionToken(loginParam)

    message = {'token': token }
    response = Response(json.dumps(message), status=201, mimetype='application/json')
    return response
    
@api_admissionControlService.route("/logout", methods = ['POST'])
def logout():
    requestId = utils.nextRequestId("logout_")

    token = common.retreiveAuthorizationToken(LOG, requestId, request.headers)

    hasRemoved : bool = authentication.removeSession(token)
    if not hasRemoved:
        reason = "Session do not exist for token: {}!".format(token)
        LOG.info("Logout [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)
    
    message = {'message': "Logout complete!" }
    response = Response(json.dumps(message), status=201, mimetype='application/json')
    return response
