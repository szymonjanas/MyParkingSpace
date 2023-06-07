import logging
import Database as db
from Server.Backend.models.users import User
from Server.Backend.models.reservation import Reservation
from Server.Backend.models.parkingslot import ParkingSlot
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from QrCodeGenerator import QrCodeGenerator

__sender__ : User = None 

def init_email_sender(user : User):
    global __sender__
    __sender__ = user

LOG = logging.getLogger(__name__)

class EmailSenderException(Exception):
    pass

class EmailSender:
    def __init__(self, login : str, ReservationId : str, requestId):
        self.login = login
        self.user : User = None
        self.reservationId = ReservationId
        self.reservation : Reservation = None
        self.parkingslot : ParkingSlot = None
        self.requestId = requestId

        self.message = None
        self.qrcodeBytes = None

    def __initDataFromDatabase__(self):
        dbUser = db.SqlSelectQuery(db.SqlTableName.USERS) \
                    .select(['*']) \
                    .where(db.SqlWhere().addCondition({User.Login: self.login}).get()) \
                    .execute(db.connector)

        if not len(dbUser):
            reason =  "User not found with login: {}".format(self.login)
            LOG.warn("Sending email attempt at [{}] aborted: {}".format(self.requestId, reason))
            raise EmailSenderException(reason)

        self.user = User.deserialize(dbUser)

        dbReservation = db.SqlSelectQuery(db.SqlTableName.RESERVATIONS) \
                            .select(["*"]) \
                            .where(db.SqlWhere().addCondition(
                                {Reservation.Login: self.login, 
                                 Reservation.ReservationId: self.reservationId}, 
                                 db.SqlConditionConcatenator.AND).get()) \
                            .execute(db.connector)

        if not len(dbReservation):
            reason =  "Reservation not found with login: {}, reservationId: {}".format(self.login, self.reservationId)
            LOG.warn("Sending email attempt at [{}] aborted: {}".format(self.requestId, reason))
            raise EmailSenderException(reason)

        self.reservation = Reservation.deserialize(dbReservation)[0]

        dbParkingSlot = db.SqlSelectQuery(db.SqlTableName.PARKINGSLOTS) \
                            .select(["*"]) \
                            .where(db.SqlWhere().addCondition({ParkingSlot.ParkingSlotId: self.reservation.ParkingSlotId}).get()) \
                            .execute(db.connector)

        if not len(dbParkingSlot):
            reason =  "Parking Slot not found with ParkingSlotId: {}".format(self.reservation.ParkingSlotId)
            LOG.warn("Sending email attempt at [{}] aborted: {}".format(self.requestId, reason))
            raise EmailSenderException(reason)

        self.parkingslot = ParkingSlot.deserialiaze(dbParkingSlot)

    def __generateQrCode__(self):
        self.qrcodeBytes = QrCodeGenerator.generateBytes(self.reservation.ReservationId)

    def __prepareMessage__(self):
        self.message = MIMEMultipart()
        self.message['From'] = __sender__.Email
        self.message['To'] = self.user.Email
        self.message['Subject'] = 'QR Code for Reservation {}'.format(self.reservation.ReservationId)
        emailBody = "Your reservation details:\ncode: {code}\ndate: {date}\nparking space number: {slot}\nparking floor: {floor}".format(
                                                                code=self.reservation.ReservationId,
                                                                date=self.reservation.ReservationDate,
                                                                slot=self.parkingslot.SlotNumber,
                                                                floor=self.parkingslot.Floor)
        self.message.attach(MIMEText(emailBody, "plain"))

        qrAttachment = MIMEImage(self.qrcodeBytes)
        qrAttachment.add_header('Content-Disposition', 'attachment', filename='reservationid.jpeg')
        self.message.attach(qrAttachment)

    def execute(self):
        global __sender__
        self.__initDataFromDatabase__()
        self.__generateQrCode__()
        self.__prepareMessage__()

        if not __sender__:
            reason = "Sender is not configured! Email will not be send!"
            LOG.warn("Sending email attempt at [{}] aborted: {}".format(self.requestId, reason))
            raise EmailSenderException(reason)
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(__sender__.Email, __sender__.Password)
            server.sendmail(__sender__.Email, __sender__.Email, self.message.as_string()) # FIXME change recipient as user.Email
