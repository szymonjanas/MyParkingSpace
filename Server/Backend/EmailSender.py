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
import config

__sender__ : User = None

def init_email_sender(address, password):
    global __sender__
    __sender__ = User(Password=password, Email=address)

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

        self.user = User.deserialize(dbUser)[0]

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

        self.parkingslot = ParkingSlot.deserialiaze_many(dbParkingSlot)[0]

    def __generateQrCode__(self):
        self.qrcodeBytes = QrCodeGenerator().generateBytes(text = self.reservation.ReservationId)

    def __prepareMessage__(self):
        self.message = MIMEMultipart()
        self.message['From'] = str(__sender__.Email)
        self.message['To'] = ', '.join(self.getEmailRecipient())
        self.message['Subject'] = '{} MyParkingSpace, New Reservation: {}'.format(self.getTestTag(), self.reservation.ReservationId)

        qrAttachment = MIMEImage(self.qrcodeBytes.getvalue())
        qrAttachment.add_header('Content-Disposition', 'attachment', filename='reservationid.jpeg')
        qrAttachment.add_header('Content-ID', 'reservationid')
        self.message.attach(qrAttachment)

        emailBody = "Hi <b>{}</b>,<br/>".format(str(self.user.Name.split(" ")[0]))
        emailBody += "You have new parking space reservation in MyParkingSpace!<br/>"
        emailBody += "-------------------------<br/>"
        emailBody += "Your reservation details:<br/>"
        emailBody += "Date: <b>{}</b><br/>".format(self.reservation.ReservationDate)
        emailBody += "Access code: <b>{}</b><br/>".format(self.reservation.ReservationId)
        emailBody += "Parking space number: <b>{}</b><br/>".format(self.parkingslot.SlotNumber)
        emailBody += "Parking floor number: <b>{}</b><br/>".format(self.parkingslot.Floor)
        emailBody += '<img src="cid:reservationid"><br/>' 
        emailBody += "Kind regards,<br/><b>MyParkingSpace</b><br/>"
        emailBody += "<br/><small><em>This reservation has been made on {}. If you did not do that, please check your account!</em></small><br/>".format(self.reservation.ReservationMadeDateTime)
        self.message.attach(MIMEText(emailBody, "html"))

    def getTestTag(self):
        if config.TEST_MODE:
            return "[TEST]"
        return ""

    def getEmailRecipient(self):
        global __sender__
        if config.TEST_MODE:
            return [__sender__.Email]
        else:
            return [__sender__.Email, self.user.Email]

    def execute(self):
        global __sender__
        LOG.info("Send email attempt at [{}] for user: {}, reservationId: {}, sender config: {}".format(
            self.requestId, self.login, self.reservationId, bool(__sender__)))
        
        if not bool(__sender__):
            reason = "Sender is not configured! Email will not be send!"
            LOG.warn("Sending email attempt at [{}] aborted: {}".format(self.requestId, reason))
            raise EmailSenderException(reason)

        self.__initDataFromDatabase__()
        self.__generateQrCode__()
        self.__prepareMessage__()
       
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(__sender__.Email, __sender__.Password)
            server.sendmail(__sender__.Email, self.getEmailRecipient(), self.message.as_string()) # FIXME change recipient as user.Email
