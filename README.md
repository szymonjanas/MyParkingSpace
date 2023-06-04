# MyParkingSpace
```
MyParkingSpace is a project for University Classes.
Project will likely be abandon as soon as we receive a grade.
```

[![Backend System Tests](https://github.com/szymonjanas/MyParkingSpace/actions/workflows/backend-system-tests.yml/badge.svg)](https://github.com/szymonjanas/MyParkingSpace/actions/workflows/backend-system-tests.yml)

Scope:
- Backend: python3 + flask
- Frontend: react
- Database: SQLite3
- CI/CD: github actions

## Services Description
### Admission Control Service
**Responsibilities:**
- Login and Register Blueprints - API,
- Generate session key and save it in local storage,
- Check session duration - remove key from local storage on timeout (session timer is equal zero),
- Decrement session timer every (1) minute,
- Provide container with current sessions, date/time of generation, time to expire,
### Space Reservation Service
**Responsibilities:**
- check if space (SpaceId) is available at given date/time range,
- reservation is possible in 15 min blocks for specific day,
pre-reservation during check - has to be confirmed in 15 min, generate ReservationId, pre-reservation is stored in local storage (ReservationContext) until it's confirmed - then is moved to database,
- make a reservation with ReservationId, for UserProfileId. Save in database reservation made for
| ReservationId | UserProfileId | Date | Time Start | Time End |
- after reservation is saved to database, ReservationId is send via email with QR Code included,
### Entry QR Code Generation Service
**Responsibilities:**
- based on confirmed reservation generate QR code for ReservationId,
### Email Sender Service
**Responsibilities:**
- creating and sending email with QR Code picture encoded,

### DATABASE
TABLE: **USERS**

`|UserProfileId|Registration date|UserName|Login|Password|Email|`

TABLE: **RESERVATIONS**

`|ReservationId|UserProfileId|Reservation Date|Time Start|Time End|Date when it was made|Time when it was made|`


[AdmissionControlClassDiagram](docs/diagrams/AdmissionControlClassDiagram.md)
