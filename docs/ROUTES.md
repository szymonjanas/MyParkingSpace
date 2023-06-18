## Server API

### `POST /api/register`
Input **json**:
```json
"Login" : "text",
"Password" : "text",
"Email" : "text",
"Name" : "text"
```
Output **json**: `201 OK`
```json 
"message": "Successful registration!"
```

### `POST /api/login`
Input **json**:
```json
"Login" : "text",
"Password" : "text"
```
Output **json**: `201 OK`
```json
"token" : "text token - 16 bytes uuid"
```

### `POST /api/logout`
Input **header**:
```json
"Authorization: token <token value>"
```
Output **json**: `201 OK`
```json
"message" : "Logout complete!"
```

### `POST /api/parking/slots`
Input **header**:
```json
"Authorization: token <token value>"
```
Input **json**:
```json
"parkingslots" : [
    {
        "SlotNumber" : "text",
        "Floor" : "text",
        "PositionX" : "text",
        "PositionY" : "text"
    }
]
```
Output: `201 OK`

### `GET /api/parking/slots/all`
Input **header**:
```json
"Authorization: token <token value>"
```
Output **json**: `201 OK`
```json
"slots" : [
    {
        "ParkingSlotId" : "text",
        "SlotNumber" : "text",
        "Floor" : "text",
        "PositionX" : "text",
        "PositionY" : "text"
    }
]
```

### `GET /api/parking/slots/<date>`
Input **header**:
```json
"Authorization: token <token value>"
```
Output **json**: `201 OK`
```json
"date" : "dd.MM.yyyy",
"slots" : [
    {
        "ParkingSlotId" : "text",
        "SlotNumber" : "text",
        "Floor" : "text",
        "PositionX" : "text",
        "PositionY" : "text",
        "isFree" : "free/taken/mine"
    }
]
```

### `POST /api/reservation/new`
Input **header**:
```json
"Authorization: token <token value>"
```
Input **json**:
```json
"reservation" : {
    "ParkingSlotId" : "text",
    "Login" : "text",
    "ReservationDate" : "text" 
}
```
Output **json**: `201 OK`
```json
"ReservationId" : "text",
"ParkingSlotId" : "text",
"Login" : "text",
"ReservationDate" : "text",
"ReservationMadeDateTime" : "text"
```

### `GET /api/reservation/all`
Input **header**:
```json
"Authorization: token <token value>"
```
Output **json**: `200 OK`
```json
[ 
    {
        "ReservationId" : "text",
        "ParkingSlotId" : "text",
        "Login" : "text",
        "ReservationDate" : "text",
        "ReservationMadeDateTime" : "text"
    }
]
```

### `DELETE /api/reservation/<ReservationId>`
Input **header**:
```json
"Authorization: token <token value>"
```
Output **json**: `201 OK`
```json
"message": "Reservation deleted!"
```

### `GET /api/reservation/qr/<ReservationId>`
Input **header**:
```json
"Authorization: token <token value>"
```
Output **file**: `201 OK`
```
image/png <reservationId qrcode>
```

### `GET /api/user`
Input **header**:
```json
"Authorization: token <token value>"
```
Output **json**: `200 OK`
```json
    "user" : {
        "RegistrationDate" : "text",
        "Name" : "text",
        "Login" : "text",
        "Email" : "text"
    }
```
