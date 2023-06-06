
class Reservation:
    def __init__(self,
                 ReservationId,
                 SlotNumber,
                 UserProfileId,
                 ReservationDate,
                 TimeStart,
                 TimeEnd,
                 DateAndTimeRegistration):
        self.ReservationId = ReservationId
        self.SlotNumber = SlotNumber
        self.UserProfileId = UserProfileId
        self.ReservationDate = ReservationDate
        self.TimeStart = TimeStart
        self.TimeEnd = TimeEnd
        self.DateAndTimeRegistration = DateAndTimeRegistration
