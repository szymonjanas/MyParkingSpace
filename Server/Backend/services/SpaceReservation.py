from flask import Blueprint, request, Response, abort
import logging
import json
from datetime import datetime
import Database
from  models.parkingslot import ParkingSlot
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
                serializedSlot["SlotNumber"],
                serializedSlot["Floor"],
                serializedSlot["PositionX"],
                serializedSlot["PositionY"])
            slots.append(slot)
        except:
            reason = "Cannot read slot from json data!"
            LOG.debug("New parking slots attempt [{}] aborted: {}".format(requestId, reason))
            abort(400, reason)

    if not len(slots):
        reason = "Slots list is empty!"
        LOG.debug("New parking slots attempt [{}] aborted: {}".format(requestId, reason))
        abort(400, reason)
    
    if not Database.get_database().clear_all_parking_slots():
        reason = "Internal database error!"
        LOG.debug("New parking slots attempt [{}] aborted: {}".format(requestId, reason))
        abort(500, reason)

    for slot in slots:
        if not Database.get_database().insert_parking_slot(slot):
            reason = "Internal database error!"
            LOG.debug("New parking slots attempt [{}] aborted: {}".format(requestId, reason))
            abort(500, reason)

    LOG.debug("New parking slots attempt [{}] finished successful!".format(requestId))
    return Response(status=201, mimetype='application/json')

@api_spaceReservation.route("/parking/slots", methods = ['GET'])
@Authentication
def parking_slots():
    requestId = utils.nextRequestId("slots_")

    serializedSlots = Database.get_database().select_parking_slots()
    slots = utils.objectsToJson(ParkingSlot.deserialiaze_many(serializedSlots))

    message = {'slots': slots }
    return Response(json.dumps(message), status=200, mimetype='application/json')

# @api_spaceReservation.route("/reservation/new", methods = ['POST'])
# @Authentication
# def new_reservation():
