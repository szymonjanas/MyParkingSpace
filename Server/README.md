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


## Running server application and tests
---
0. Preparation, install localy: `python3`, `python3-pip`, `python3-venv`
1. Build virual enviroment in folder `MyParkingSpace`: `python3 -m venv venv`
2. Source enviroment: `source ./venv/bin/activate` (linux) `./venv/Scripts/activate` (windows)
3. Install project: `pip3 install -e .`
4. Install dependencies: `pip3 install -r Server/requirements.txt`
4. Go to folder `Server` and type: 
    - for run tests: `python3 BackendSystemTests`
    - for run app: `python3 Backend`

### Supported Backend flags
---
```
--ipaddress <address>
--logfilepath <path>
--loglevel <DEBUG/INFO/ERROR>
--databasepath <path>
--newdatabase
--emailaddress <address>
--emailpassword <password>
--emailconfig (get email setting from config.json)
--testmode (turn on TEST_MODE)
```

### Supported BackendSystemTests flags
---
```
--testcase <testcase simple regex>
--loglevel <DEBUG/INFO/ERROR>
--os <linux/windows/ci-linux>
--emailconfig (get email settings from config.json)
--emailaddress <email>
--emailpassword <password>
```