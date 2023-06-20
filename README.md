# MyParkingSpace
```
MyParkingSpace is a project for University Classes.
Project will likely be abandon as soon as we receive a grade.
Edit: We got 5.0 🥇
```

[![Backend System Tests](https://github.com/szymonjanas/MyParkingSpace/actions/workflows/backend-system-tests.yml/badge.svg)](https://github.com/szymonjanas/MyParkingSpace/actions/workflows/backend-system-tests.yml)
[![Build React Frontend](https://github.com/szymonjanas/MyParkingSpace/actions/workflows/frontend-build.yml/badge.svg)](https://github.com/szymonjanas/MyParkingSpace/actions/workflows/frontend-build.yml)

---

Application run and tested under `ubuntu-20.04`.

Current version: `v0.9`

---

### Description:
```
Fullstack application to reserve parking slot for a day and generate parking access code.
Allow user to register, login, pick a date, pick a slot, and create, view or delete reservation.
```

### Scope
- `Backend: python3 + flask`
- `Frontend: react + MUI`
- `Database: SQLite3`
- `CI: github actions`
 
### Pages

- [APPLICATION SCREENSHOTS](docs/SCREENSHOTS.md)

- [BACKEND API ROUTES](docs/ROUTES.md)

- [BUILD AND RUN APPLICATION](docs/RUN_APPLICATION.md)

---

## Services Description
### Admission Control Service
**Responsibilities:**
- login and register user,
- generate session key and save it in local storage,
- remove key from local storage on logout,
- provide container with current sessions.

### Space Reservation Service

**Responsibilities:**
- check if parking slot is available at given date (format `dd.mm.yyyy`),
- reservation is possible in for specific day and slot,
- create reservation for user,
- delete reservation for user,
- after reservation is saved to database: email notification is sent with QR Code included,
- after reservation is deleted from database: email notification is sent.

### Entry QR Code Generation Service
**Responsibilities:**
- based on confirmed reservation generate QR code from ReservationId,
### Email Sender Service
**Responsibilities:**
- creating and sending email notification with QR Code picture included,

## Database tables description
- TABLE: **USERS**
    |RegistrationDate|Name|Login|Password|Email|
    |---|---|---|---|---|


- TABLE: **RESERVATIONS**
    |ReservationId|ParkingSlotId|Login|ReservationDate|ReservationMadeDateTime|
    |---|---|---|---|---|

- TABLE: **PARKINGSLOTS**
    |ParkingSlotId|SlotNumber|Floor|PositionX|PositionY|
    |---|---|---|---|---|
