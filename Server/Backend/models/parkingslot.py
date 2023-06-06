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
    def deserialize(array):
        return ParkingSlot(
            array[0],
            array[1],
            array[2],
            array[3],
            array[4]
        )

    @staticmethod
    def deserialiaze_many(arrayOfArray):
        output = []
        for item in arrayOfArray:
            output.append(ParkingSlot.deserialize(item))
        return output
