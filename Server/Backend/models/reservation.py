from Server.Backend.models.model import Model

class Reservation(Model):
    ReservationId = "ReservationId"
    ParkingSlotId = "ParkingSlotId"
    UserProfileId = "UserProfileId"
    ReservationDate = "ReservationDate"
    ReservationMadeDateTime = "ReservationMadeDateTime"

    def __init__(self,
                 ReservationId : str = "",
                 ParkingSlotId : str = "",
                 UserProfileId : str = "",
                 ReservationDate : str = "",
                 ReservationMadeDateTime : str = ""):
        self.ReservationId = ReservationId
        self.ParkingSlotId = ParkingSlotId
        self.UserProfileId = UserProfileId
        self.ReservationDate = ReservationDate
        self.ReservationMadeDateTime = ReservationMadeDateTime
