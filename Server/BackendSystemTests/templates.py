
class User:
    def __init__(self, login, password, email, name):
        self.login = login
        self.password = password
        self.email = email
        self.name = name

def t_user() -> User:
    return User(
            "pkowalski",
            "piotrkowalski123",
            "piotr.kowalski@poczta.com",
            "Piotr Kowalski"
        )

class ParkingSlot:
    def __init__(self,
                 SlotNumber,
                 Floor,
                 PositionX,
                 PositionY):
        self.SlotNumber = SlotNumber
        self.Floor = Floor
        self.PositionX = PositionX
        self.PositionY = PositionY
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
                if len(slot) == 3: # entrance slot
                    slots.append(
                        ParkingSlot(-1, floorIdx, slot[0], slot[1]).__dict__
                    )
                else:
                    slots.append(
                        ParkingSlot(idx, floorIdx, slot[0], slot[1]).__dict__
                    )
        return slots

t_parkingSlots = generateParkingSlots()
