from flask import Blueprint, request, Response
from abort import abort
import logging
import json
import datetime
import Database as db
from models.users import User
import authentication as auth
from services.common import retreiveAuthorizationToken, validateParameters, isSessionValid
from utils import toTuple, nextRequestId
from authentication import Authentication

api_admissionControlService = Blueprint("Admission Control Service", __name__)

LOG = logging.getLogger(__name__)

@api_admissionControlService.route("/api/register", methods = ['POST'])
def register():

    registerData = request.json
    requestId = nextRequestId("reg_")
    registerData = dict(registerData)
    LOG.info("Registration attempt [{}] with data: {}".format(requestId, request.json))
    
    def abortWith(reason):
        LOG.warn("Registration [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    validateParameters(registerData, abortWith, [User.Login, User.Password, User.Email, User.Name])
    
    dbRows = db.SqlSelectQuery(db.SqlTableName.USERS) \
                .select((User.Login, User.Email)) \
                .where(db.SqlWhere() \
                    .And({User.Login: registerData[User.Login]}) \
                    .Or({User.Email: registerData[User.Email]}) \
                    .get()) \
                .execute(db.connector)
    
    if len(dbRows) > 0:
        if len(list(filter(lambda item: item[0]==registerData[User.Login], dbRows))):
            reason = 'User with login {} is already registered!'.format(registerData[User.Login])
            LOG.warn("Registration [{}] aborted: {}".format(requestId, reason))
            abort(400, reason)
        if len(list(filter(lambda item: item[1]==registerData[User.Email], dbRows))):
            reason = 'User with email {} is already registered!'.format(registerData[User.Email])
            LOG.warn("Registration [{}] aborted: {}".format(requestId, reason))
            abort(400, reason)

    try:
        user = User(
            None,
            registerData[User.Name],
            registerData[User.Login],
            registerData[User.Password],
            registerData[User.Email]
        )
    except Exception as ex:
        LOG.warn("Registration [{}] aborted: {}".format(requestId, ex))
        abort(400, ex)

    user.RegistrationDate = datetime.datetime.now().strftime("%d.%m.%Y")

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

@api_admissionControlService.route("/api/login", methods = ['POST'])
def login():
    loginData = request.json
    requestId = nextRequestId("login_")
    LOG.info("Login attempt [{}] with data: {}".format(requestId, loginData))

    loginData = dict(loginData)

    def abortWith(reason):
        LOG.warn("Login [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    validateParameters(loginData, abortWith, [User.Login, User.Password])

    loginParam = loginData[User.Login]
    try:
        dbRows = db.SqlSelectQuery(db.SqlTableName.USERS) \
                        .select((User.Login, User.Password)) \
                        .where(db.SqlWhere() \
                                .And({User.Login: loginParam}).get()) \
                        .execute(db.connector)
    except Exception as ex:
        LOG.error("Login [{}] aborted: {}".format(requestId, ex))
        abort(400, ex)

    if (len(dbRows) == 0):
        reason = "User with login {} is not registered!".format(loginParam)
        LOG.info("Login [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    password = dbRows[0][1]
    if not (password == loginData[User.Password]):
        reason = "Wrong password for user: {}!".format(loginParam)
        LOG.info("Login [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    token = auth.generateSessionToken(loginParam)

    message = {'token': token }
    response = Response(json.dumps(message), status=201, mimetype='application/json')
    return response

@api_admissionControlService.route("/api/logout", methods = ['POST'])
def logout():
    requestId = nextRequestId("logout_")

    token = retreiveAuthorizationToken(LOG, requestId, request.headers)
    LOG.info("Logout attempt [{}] with token: {}".format(requestId, token))
    hasRemoved : bool = auth.removeSession(token)
    if not hasRemoved:
        reason = "Session do not exist for token: {}!".format(token)
        LOG.info("Logout [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)
    
    message = {'message': "Logout complete!" }
    response = Response(json.dumps(message), status=201, mimetype='application/json')
    return response

@api_admissionControlService.route("/api/user", methods = ['GET'])
@Authentication
def get_user_info():
    requestId = nextRequestId("userinfo_")

    login, _ = isSessionValid(LOG, requestId, request.headers)
    LOG.info("Get user info attempt [{}] for login: {}".format(requestId, login))

    userDetails = db.SqlSelectQuery(db.SqlTableName.USERS) \
                    .select([User.RegistrationDate, User.Name, User.Login, User.Email]) \
                    .where(db.SqlWhere().And({User.Login : login}).get()) \
                    .execute(db.connector)
    
    userDetails = User(
        userDetails[0][0],
        userDetails[0][1],
        userDetails[0][2],
        "***",
        userDetails[0][3],
    ).__dict__

    message = {'user': userDetails }
    response = Response(json.dumps(message), status=200, mimetype='application/json')
    return response
