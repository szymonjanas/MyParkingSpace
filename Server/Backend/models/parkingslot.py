from Server.Backend.models.model import Model

class ParkingSlot(Model):
    ParkingSlotId = "ParkingSlotId"
    SlotNumber = "SlotNumber"
    Floor = "Floor"
    PositionX = "PositionX"
    PositionY = "PositionY"

    def __init__(self,
                 ParkingSlotId = "",
                 SlotNumber = "",
                 Floor = "",
                 PositionX = "",
                 PositionY = ""):
        self.ParkingSlotId = ParkingSlotId
        self.SlotNumber = SlotNumber
        self.Floor = Floor
        self.PositionX = PositionX
        self.PositionY = PositionY

    @staticmethod
    def deserialize(item):
        return ParkingSlot(
            item[0],
            item[1],
            item[2],
            item[3],
            item[4]
        )

    @staticmethod
    def deserialiaze_many(arrayOfArray):
        output = []
        for item in arrayOfArray:
            output.append(ParkingSlot.deserialize(item))
        return output
