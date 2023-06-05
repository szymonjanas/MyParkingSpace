
class ParkingSlot:
    def __init__(self,
                 SlotNumber = "",
                 PositionX = "",
                 PositionY = ""):
        self.SlotNumber = SlotNumber
        self.PositionX = PositionX
        self.PositionY = PositionY

    def toTuple(self):
        return (
            self.SlotNumber,
            self.PositionX,
            self.PositionY
        )
    

    @staticmethod
    def toNamesFixture():
        return '{}, {}, {}'.format(
            ParkingSlot.dbSlotNumber(),
            ParkingSlot.dbPositionX(),
            ParkingSlot.dbPositionY()
        )

    @staticmethod
    def dbValues():
        return "?,?,?"

    @staticmethod
    def dbSlotNumber():
        return "SlotNumber"
    
    @staticmethod
    def dbPositionX():
        return "PositionX"

    @staticmethod
    def dbPositionY():
        return "PositionY"

    @staticmethod
    def deserialize(array, fixture = None):
        if len(array) == 4:
            return ParkingSlot(
                array[0],
                array[1],
                array[2],
            )
        else:
            if not fixture:
                return
            SlotNumber = ""
            ReservationId = ""
            PositionX = ""
            PositionY = ""
            idx = 0
            if ParkingSlot.dbSlotNumber() in fixture:
                SlotNumber = array[idx]
                idx += 1

            if ParkingSlot.dbPositionX() in fixture:
                PositionX = array[idx]
                idx += 1
            if ParkingSlot.dbPositionY() in fixture:
                PositionY = array[idx]

            return ParkingSlot(
                SlotNumber=SlotNumber,
                PositionX=PositionX,
                PositionY=PositionY
            )

    @staticmethod
    def deserialiaze_many(arrayOfArray):
        output = []
        for item in arrayOfArray:
            output.append(ParkingSlot.deserialize(item))
        return output

    @staticmethod
    def toJson(array):
        output = []
        for item in array:
            output.append(item.__dict__)
        return output
        
