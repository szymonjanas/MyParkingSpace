from flask import Blueprint, request, Response, abort
import logging
import json
from datetime import datetime
import Database as db
from  models.parkingslot import ParkingSlot
from models.reservation import Reservation
import utils
from authentication import Authentication
from services import common


api_spaceReservation = Blueprint("Space Reservation", __name__)

LOG = logging.getLogger(__name__)

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

    message = {'slots': slots }
    return Response(json.dumps(message), status=200, mimetype='application/json')

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
            ParkingSlotId=   reservationData["ParkingSlotId"],
            UserProfileId=   reservationData["UserProfileId"],
            ReservationDate= reservationData["ReservationDate"]
        )
    except:
        reason = "Cannot read reservation parameters from json data!"
        LOG.debug("New reservation attempt [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)
    
    isReserved = db.SqlSelectQuery(db.SqlTableName.RESERVATIONS) \
                    .select((Reservation.ParkingSlotId, Reservation.ReservationDate)) \
                    .where(db.SqlWhereBuilder()
                                .addCondition({ Reservation.ReservationDate: reservation.ReservationDate }).get()) \
                    .execute(db.connector)

    if len(isReserved):
        reason = "Parking slot at given date is already taken!"
        LOG.debug("New reservation attempt [{}] aborted: {}".format(requestId, reason))
        abort(409, reason)

    reservation.ReservationId = "69"

    todayDateTime = datetime.now().strftime("%d.%m.%Y %H:%M")
    reservation.ReservationMadeDateTime = todayDateTime
    db.SqlInsertQuery(db.SqlTableName.RESERVATIONS) \
        .insert(reservation) \
        .execute(db.connector)

    message = {'message': "New reservation created!" }
    return Response(json.dumps(message), status=201, mimetype='application/json')
