from Server.Backend.models.model import Model
from Server.Backend.models.users import User
from Server.Backend.models.parkingslot import ParkingSlot

class Reservation(Model):
    ReservationId = "ReservationId"
    ParkingSlotId = ParkingSlot.ParkingSlotId
    Login = User.Login
    ReservationDate = "ReservationDate"
    ReservationMadeDateTime = "ReservationMadeDateTime"

    def __init__(self,
                 ReservationId : str = "",
                 ParkingSlotId : str = "",
                 Login : str = "",
                 ReservationDate : str = "",
                 ReservationMadeDateTime : str = ""):
        self.ReservationId = ReservationId
        self.ParkingSlotId = ParkingSlotId
        self.Login = Login
        self.ReservationDate = ReservationDate
        self.ReservationMadeDateTime = ReservationMadeDateTime

    @staticmethod
    def deserialize(array : list, func = lambda item : item):
        output = []
        for item in array:
            output.append(
                func(Reservation(
                        item[0],
                        item[1],
                        item[2],
                        item[3],
                        item[4])
                )
            )
        return output
