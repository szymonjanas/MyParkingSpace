from flask import Blueprint, request, Response, abort, send_file
import logging
import json
from datetime import datetime
import Database as db
from  models.parkingslot import ParkingSlot
from models.reservation import Reservation
from models.users import User
import utils
from authentication import Authentication
from services.common import isSessionValid
import random
import string
from QrCodeGenerator import QrCodeGenerator

api_spaceReservation = Blueprint("Space Reservation", __name__)

LOG = logging.getLogger(__name__)

def __generateLetters__(num = 4):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(num))

def nextReservationId(reservationIdList : list):
    reservationId = __generateLetters__()
    while reservationId in reservationIdList:
        reservationId = __generateLetters__()
    return reservationId

@api_spaceReservation.route("/parking/slots/new", methods = ['POST'])
@Authentication
def new_parking_slots():
    # FIXME parking slots initiation should belongs to administrator token only!
    requestId = utils.nextRequestId("new_slots_")
    LOG.warn("New parking slots attempt [{}] with data: {}".format(requestId, request.json))
    try:
        parkingSlotsData = request.json["parkingslots"]
    except:
        reason = "Json data not found!"
        LOG.debug("New parking slots attempt [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    slots = []
    for serializedSlot in parkingSlotsData:
        try:
            slot = ParkingSlot(
                    SlotNumber= serializedSlot["SlotNumber"],
                    Floor=      serializedSlot["Floor"],
                    PositionX=  serializedSlot["PositionX"],
                    PositionY=  serializedSlot["PositionY"])
            slots.append(slot)
        except:
            reason = "Cannot read slot from json data!"
            LOG.debug("New parking slots attempt [{}] aborted: {}".format(requestId, reason))
            abort(400, reason)

    if not len(slots):
        reason = "Slots list is empty!"
        LOG.debug("New parking slots attempt [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    if not db.SqlDeleteQuery(db.SqlTableName.PARKINGSLOTS).delete().execute(db.connector):
        reason = "Internal database error!"
        LOG.debug("New parking slots attempt [{}] aborted: {}".format(requestId, reason))
        abort(500, reason)


    for slot in slots:
        slot.ParkingSlotId = '{}-{}'.format(slot.Floor, slot.SlotNumber)
        if not db.SqlInsertQuery(db.SqlTableName.PARKINGSLOTS) \
                    .insert(slot) \
                    .execute(db.connector):
            reason = "Internal database error!"
            LOG.debug("New parking slots attempt [{}] aborted: {}".format(requestId, reason))
            abort(500, reason)

    LOG.debug("New parking slots attempt [{}] finished successful!".format(requestId))
    return Response(status=201, mimetype='application/json')

@api_spaceReservation.route("/parking/slots", methods = ['GET'])
@Authentication
def parking_slots():
    requestId = utils.nextRequestId("slots_")
    serializedSlots = db.SqlSelectQuery(db.SqlTableName.PARKINGSLOTS) \
                            .select(('*')) \
                            .execute(db.connector)
    slots = utils.objectsToJson(ParkingSlot.deserialiaze_many(serializedSlots))

    message = json.dumps({'slots': slots })
    return Response(response=message, status=200, mimetype='application/json')

@api_spaceReservation.route("/reservation/new", methods = ['POST'])
@Authentication
def new_reservation():
    requestId = utils.nextRequestId("new_reservation_")
    LOG.info("New reservation attempt [{}] with data: {}".format(requestId, request.json))
    try:
        reservationData = request.json["reservation"]
    except:
        reason = "Json data not found!"
        LOG.debug("New reservation attempt [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    try:
        reservation = Reservation(
            ParkingSlotId=reservationData[Reservation.ParkingSlotId],
            Login=reservationData[Reservation.Login],
            ReservationDate=reservationData[Reservation.ReservationDate]
        )
    except:
        reason = "Cannot read reservation parameters from json data!"
        LOG.debug("New reservation attempt [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    isUser = db.SqlSelectQuery(db.SqlTableName.USERS) \
                .select([User.Login]) \
                .where(db.SqlWhere().addCondition({User.Login: reservation.Login}).get()) \
                .execute(db.connector)
    
    if not len(isUser):
        reason = "Login do not exist!"
        LOG.debug("New reservation attempt [{}] aborted: {}".format(requestId, reason))
        abort(401, reason)

    isReserved = db.SqlSelectQuery(db.SqlTableName.RESERVATIONS) \
                    .select((Reservation.ParkingSlotId, Reservation.ReservationDate)) \
                    .where(db.SqlWhere() \
                                .addCondition({ Reservation.ReservationDate: reservation.ReservationDate }).get()) \
                    .execute(db.connector)

    if len(isReserved):
        reason = "Parking slot at given date is already taken!"
        LOG.debug("New reservation attempt [{}] aborted: {}".format(requestId, reason))
        abort(409, reason)

    dbReservationsIds = db.SqlSelectQuery(db.SqlTableName.RESERVATIONS) \
                        .select([Reservation.ReservationId]) \
                        .execute(db.connector)
    
    reservation.ReservationId = nextReservationId(dbReservationsIds)
    reservation.ReservationMadeDateTime = datetime.now().strftime("%d.%m.%Y %H:%M")

    db.SqlInsertQuery(db.SqlTableName.RESERVATIONS) \
        .insert(reservation) \
        .execute(db.connector)

    message = json.dumps(reservation.__dict__)
    return Response(response=message, status=201, mimetype='application/json')


@api_spaceReservation.route("/reservation/all", methods = ['GET'])
@Authentication
def get_all_reservation():
    requestId = utils.nextRequestId("get_all_reservations")
    login, token = isSessionValid(LOG, requestId, request.headers)
    LOG.info("Get all reservations attempt [{}] for user: {}".format(requestId, login))

    dbAllReservations = db.SqlSelectQuery(db.SqlTableName.RESERVATIONS) \
                        .select(['*']) \
                        .where(db.SqlWhere() \
                                    .addCondition({Reservation.Login: login}) \
                                    .get()) \
                        .execute(db.connector)

    dictAllReservations = Reservation.deserialize(dbAllReservations)

    message = json.dumps(dictAllReservations)
    return Response(message, 200, content_type='application/json')
# check if return empty list

@api_spaceReservation.route("/reservation/<ReservationId>", methods = ['DELETE'])
@Authentication
def delete_reservation(ReservationId):
    requestId = utils.nextRequestId("new_reservation_")
    login, token = isSessionValid(LOG, requestId, request.headers)
    LOG.info("Delete reservation attempt [{}] for user: {}, ReservationId: {}".format(requestId, login, ReservationId))

    dbAllReservations = db.SqlSelectQuery(db.SqlTableName.RESERVATIONS) \
                        .select(['*']) \
                        .where(db.SqlWhere() \
                                    .addCondition({Reservation.ReservationId: ReservationId}) \
                                    .get()) \
                        .execute(db.connector)

    if not len(dbAllReservations):
        reason = "Reservation does not exits!"
        LOG.debug("Delete reservation attempt [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    db.SqlDeleteQuery(db.SqlTableName.RESERVATIONS) \
        .delete() \
        .where(db.SqlWhere() \
                    .addCondition({Reservation.ReservationId: ReservationId}) \
                    .get()) \
        .execute(db.connector)

    message = {"message": "Reservation deleted!"}
    return Response(message, 201, content_type='application/json')

@api_spaceReservation.route("/reservation/qr/<ReservationId>", methods = ['GET'])
@Authentication
def qr_code_for_reservation(ReservationId):
    requestId = utils.nextRequestId("qr_reservation_")
    login, token = isSessionValid(LOG, requestId, request.headers)
    LOG.info("Qr Code generation attempt [{}] for user: {}, ReservationId: {}".format(requestId, login, ReservationId))

    dbAllReservations = db.SqlSelectQuery(db.SqlTableName.RESERVATIONS) \
                        .select(['*']) \
                        .where(db.SqlWhere() \
                                    .addCondition({Reservation.ReservationId: ReservationId}) \
                                    .get()) \
                        .execute(db.connector)

    if not len(dbAllReservations):
        reason = "Reservation does not exits!"
        LOG.debug("Delete reservation attempt [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)

    qrImgByteBuff = QrCodeGenerator().generateBytes(ReservationId)
    return send_file(qrImgByteBuff, mimetype='image/png')
