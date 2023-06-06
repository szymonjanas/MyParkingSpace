
class ParkingSlot:
    SlotNumber = "SlotNumber"
    Floor = "Floor"
    PositionX = "PositionX"
    PositionY = "PositionY"

    def __init__(self,
                 SlotNumber = "",
                 Floor = "",
                 PositionX = "",
                 PositionY = ""):
        self.SlotNumber = SlotNumber
        self.Floor = Floor
        self.PositionX = PositionX
        self.PositionY = PositionY

    @staticmethod
    def deserialize(array, fixture = None):
        if len(array) == 4:
            return ParkingSlot(
                array[0],
                array[1],
                array[2],
                array[3]
            )
        else:
            if not fixture:
                return
            SlotNumber = ""
            Floor = ""
            PositionX = ""
            PositionY = ""
            idx = 0
            if ParkingSlot.SlotNumber in fixture:
                SlotNumber = array[idx]
                idx += 1

            if ParkingSlot.Floor in fixture:
                Floor = array[idx]
                idx += 1

            if ParkingSlot.PositionX in fixture:
                PositionX = array[idx]
                idx += 1
            if ParkingSlot.PositionY in fixture:
                PositionY = array[idx]

            return ParkingSlot(
                SlotNumber=SlotNumber,
                Floor=Floor,
                PositionX=PositionX,
                PositionY=PositionY
            )

    @staticmethod
    def deserialiaze_many(arrayOfArray):
        output = []
        for item in arrayOfArray:
            output.append(ParkingSlot.deserialize(item))
        return output
