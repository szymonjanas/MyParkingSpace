from Server.Backend.models.reservation import Reservation
from Server.Backend.models.parkingslot import ParkingSlot
from Server.Backend.models.users import User

def t_user() -> dict:
    user = User(
            RegistrationDate = None,
            Name = "Piotr Kowalski",
            Login = "pkowalski",
            Password = "piotrkowalski123",
            Email = "piotr.kowalski@poczta.com"
        ).__dict__
    user.pop(User.RegistrationDate)
    return user

# [x, y]
ParkingMap = [
           [2,1],               [5,1],
    [1,2],        [3,2], [4,2],        [6,2],
    [1,3],        [3,3], [4,3],        [6,3],
    [1,4],        [3,4], [4,4],        [6,4],
    [1,5],                             [6,5],
    [1,6],[2,6,-1],[3,6], [4,6], [5,6]
]

def generateParkingSlots(Floor = 1):
        slots = []
        for floorIdx in range(Floor):
            for idx, slot in enumerate(ParkingMap):
                tslot = None
                if len(slot) == 3: # entrance slot
                    tslot = ParkingSlot("", -1, floorIdx, slot[0], slot[1]).__dict__
                else:
                    tslot = ParkingSlot("", idx, floorIdx, slot[0], slot[1]).__dict__
                tslot.pop(ParkingSlot.ParkingSlotId)
                slots.append(tslot)
        return slots

t_parkingSlots = generateParkingSlots()


def t_reservation(login):

    reservation : dict = Reservation(
        ReservationId=None,
        ParkingSlotId="1-12",
        Login=login,
        ReservationDate="12-06-2023",
        ReservationMadeDateTime=None 
    ).__dict__

    reservation.pop(Reservation.ReservationId)
    reservation.pop(Reservation.ReservationMadeDateTime)
     
    return reservation
