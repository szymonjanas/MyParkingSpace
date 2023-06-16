import * as React from 'react';
import { ContentBox } from '../ContextBox';
import { useProfile } from '../database/UserProfile';
import DatePicker, { registerLocale, setDefaultLocale } from 'react-datepicker';
import { useState } from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import pl from 'date-fns/locale/pl';
import { CheckCircleOutline } from '@mui/icons-material';
import { Button, Dialog, DialogTitle, Typography } from '@mui/material';
import { GarageOutlined } from '@mui/icons-material';
import * as request from '../requests';
registerLocale('pl', pl)
setDefaultLocale('pl')

const CENTER_STYLE = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center"
}

export function Home() {

  const { userProfile } = useProfile();
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [myreservations, setMyReservations] = useState([]);

  const formatDate = (date) => {
    return date.toLocaleDateString('pl-PL', { day: '2-digit', month: '2-digit', year: 'numeric' });
  };

  const MyReservations = () => {
    const getMyReservations = () => {
      request.sendRequestForGetAllReservations(userProfile.token)
        .then((reservations) => {
          console.log(reservations)
          setMyReservations(myreservations)
        })
    }

    React.useEffect(getMyReservations, [])

    return (
      <>
      </>
    )
  }


  const Calendar = () => {
    const handleDateChange = (date) => {
      setSelectedDate(date);
      console.log(formatDate(date))
    };

    return (
      <div>
        <h1>My Calendar</h1>
        <DatePicker dateFormat="dd.MM.yyyy" selected={selectedDate} onChange={handleDateChange} />
      </div>
    );
  };

  const [parkingslots2D, setParkingSlots] = useState([])

  const updateParkingSlots = () => {
    request.sendRequestForParkingSlotsByDate(userProfile.token, formatDate(selectedDate))
      .then((parkingSlotsJson) => {
        console.log("Update parking slots!")
        if (![...parkingSlotsJson].length) {
          return
        }
        const maxX = Math.max(...parkingSlotsJson.map((space) => space.PositionX));
        const maxY = Math.max(...parkingSlotsJson.map((space) => space.PositionY));

        const parking2D = new Array(maxY + 1).fill(null).map(() => new Array(maxX + 1).fill(null));

        parkingSlotsJson.forEach((space) => {
          parking2D[space.PositionY][space.PositionX] = space;
        });

        setParkingSlots(parking2D)
      })
  }
  React.useEffect(updateParkingSlots, [myreservations, selectedDate])

  const [isNewReservationFormOpen, setNewReservationFormOpen] = React.useState(false);
  const [currentSlot, setCurrentSlot] = React.useState(null);

  const NewReservationForm = () => {
    const handleOnClose = () => {
      setNewReservationFormOpen(false);
    }

    const performReservation = () => {
      const reservation = {
        "reservation": {
          "ParkingSlotId": currentSlot === null ? "" : currentSlot.ParkingSlotId,
          "Login": userProfile === null ? "" : userProfile.username,
          "ReservationDate": selectedDate === null ? "" : formatDate(selectedDate)
        }
      }
      request.sendRequestForNewReservation(userProfile.token, reservation)
      .then(() => updateParkingSlots());
      handleOnClose()
    }

    return (
      <>
        <Dialog
          open={isNewReservationFormOpen}
          onClose={handleOnClose}
          PaperProps={{
            className: "gradient-border",
            style: {
              height: "40vh",
              width: "40vh",
              borderRadius: "70vh",
              borderStyle: "solid",
              borderWidth: "medium",
              textAlign: "center"
            },

            elevation: 0
          }}
        >

          <DialogTitle sx={{
            textAlign: "center",
            color: "DodgerBlue"
          }} >
            <GarageOutlined fontSize="large" color="info" />
            <Typography variant="subtitle1">
              New reservation
            </Typography>
          </DialogTitle>
          <Typography variant="subtitle1">
            Parking space number: <b>{currentSlot === null ? "" : currentSlot.ParkingSlotId}</b>
          </Typography>
          <Typography variant="subtitle1">
            Parking space location: <b>{currentSlot === null ? "" : currentSlot.SlotNumber}</b>
          </Typography>
          <Typography variant="subtitle1">
            Parking space floor: <b>{currentSlot === null ? "" : currentSlot.Floor}</b>
          </Typography>
          <Button
            onClick={performReservation}
            startIcon={<CheckCircleOutline />}
            color="success"
            fullWidth
            sx={{ paddingBottom: "4vh", marginTop: "auto" }}
          >
            <b>Reserve</b>
          </Button>
        </Dialog>
      </>
    );
  };

  const ParkingSlots = () => {
    console.log("Get colors for pa parking slots!")
    const getColor = (space) => {
      if (space.SlotNumber === '-1')
        return "peru"

      if (space.isFree === "free")
        return "palegreen"
      else if (space.isFree === "mine")
        return "forestgreen"
      else
        return "lightgrey"

    }

    const isParkingSpaceMineAtCurrentDate = () => {
      return parkingslots2D.some((xItem) => xItem.some((yItem) => {
        if (yItem !== null)
          if (yItem.isFree === 'mine')
            return true;
      }))
    }

    const deserializeIsFree = (space) => {
      if (space.isFree === 'mine')
        return true
      if (isParkingSpaceMineAtCurrentDate())
        return false

      else if (space.isFree === "free")
        return true
      else
        return false
    }

    const setShowReservationForm = (slot) => {
      console.log("showReservationForm")

    }

    const openNewReservationForm = (slot) => {
      console.log("newReservationForm")
      setNewReservationFormOpen(true);
      setCurrentSlot(slot);

    }

    const onClickParkingSlotButtonAction = (slot) => {
      if (isParkingSpaceMineAtCurrentDate())
        if (slot.isFree === "mine") {
          return setShowReservationForm(slot)
        }
      if (slot.isFree === "free") {
        return openNewReservationForm(slot)
      }
    }

    return (
      <div>
        <table>
          <tbody>
            {parkingslots2D.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {row.map((space, columnIndex) => (
                  <td key={columnIndex}>
                    {space && (
                      <Button
                        variant="contained"
                        style={{
                          backgroundColor: getColor(space), margin: 5, color: "black",
                          display: 'flex',
                          flexDirection: 'column',
                          alignItems: 'center',
                          justifyContent: 'center',
                          border: 'none',
                          cursor: 'pointer'
                        }}
                        disabled={!deserializeIsFree(space)}
                        onClick={() => onClickParkingSlotButtonAction(space)}
                      >
                        <div ><b>{space.SlotNumber === -1 ? <b>Entry</b> : space.ParkingSlotId}</b></div>
                        <div ><small>{space.isFree}</small></div>
                      </Button>
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );

  };

  return (
    <>
      <ContentBox>
        <Typography align="center">
          Welcome <b>{userProfile.username}</b> in MyParkingSpace!
        </Typography>
        <MyReservations />
        <div style={CENTER_STYLE}>
          <Calendar />
        </div>
        <div style={CENTER_STYLE}>
          <ParkingSlots />
        </div>
      </ContentBox>
      <NewReservationForm />
    </>
  );

}
