import * as React from 'react';
import { ContentBox } from '../ContextBox';
import { useProfile } from '../database/UserProfile';
import DatePicker, { registerLocale, setDefaultLocale } from 'react-datepicker';
import { useState } from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import pl from 'date-fns/locale/pl';
import { CheckCircleOutline, DeleteForever, CalendarMonth, Today } from '@mui/icons-material';
import { Button, Dialog, DialogTitle, Typography } from '@mui/material';
import { GarageOutlined } from '@mui/icons-material';
import * as request from '../requests';
import { Card, CardContent, IconButton, DialogContent, DialogActions } from '@mui/material';
import { QrCode } from '@mui/icons-material';
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
  const [showAllReservations, setShowAllReservations] = useState(false);

  const [openConfAlert, setConfAlert] = React.useState(false);
  const [onConfAlertAcceptCallback, setConfAlertOnAcceptCallback] = React.useState(() => { return () => { } });
  const [confAlertAcceptText, setConfAlertAcceptText] = React.useState("");
  const [confTitleAlertText, setConfTitleAlertText] = React.useState("");

  const triggerConfAlert = (confAlertText, confTitleAlertText, onAcceptCallback) => {
    setConfAlertAcceptText(confAlertText);
    setConfTitleAlertText(confTitleAlertText);
    setConfAlertOnAcceptCallback(() => { return onAcceptCallback })
    setConfAlert(true);
  }

  const ConfirmationAlert = () => {

    const triggerClose = () => {
      setConfAlert(false)
    };

    const triggerAccept = () => {
      onConfAlertAcceptCallback()
      triggerClose();
    }

    return (
      <>
        <Dialog
          open={openConfAlert}
          onClose={triggerClose}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">
            {confTitleAlertText}
          </DialogTitle>
          <DialogActions style={{ display: 'flex', justifyContent: 'center' }}>
            <Button onClick={triggerClose} autoFocus>
              Cancel
            </Button>
            <Button onClick={triggerAccept} href="/" style={{ marginLeft: '2vh' }} >
              {confAlertAcceptText}
            </Button>
          </DialogActions>

        </Dialog>
      </>
    );
  }

  const formatDate = (date) => {
    return date.toLocaleDateString('pl-PL', { day: '2-digit', month: '2-digit', year: 'numeric' });
  };

  const updateMyReservations = () => {
    request.sendRequestForGetAllReservations(userProfile.token)
      .then((reservations) => {
        setMyReservations(reservations)
      })
  }
  React.useEffect(updateMyReservations, [])

  const changeReservationCardView = () => {
    setShowAllReservations(!showAllReservations);
  }

  const [openQrDialog, setOpenQrDialog] = useState(false);
  const [qrCodeImg, setQrCodeImg] = useState(null)

  const triggerQrCodeDialog = (reservation) => {
    request.sendRequestForGetReservationQrCode(userProfile.token, reservation.ReservationId)
      .then((image) => {
        setQrCodeImg(URL.createObjectURL(image));
      })
    setOpenQrDialog(true);
  }

  const QrCodeDialog = ({ imageUrl }) => {

    const handleClose = () => {
      setOpenQrDialog(false);
    };

    return (
      <>
        <Dialog open={openQrDialog} onClose={handleClose}>
          <DialogContent>
            <img src={qrCodeImg} alt="QrCode" />
          </DialogContent>
        </Dialog>
      </>
    );
  };

  const triggerDeleteReservation = (ReservationId) => {
    const deleteReservation = () => {
      request.sendRequestForDeleteReservation(userProfile.token, ReservationId)
        .then(() => {
          updateParkingSlots();
          updateMyReservations();
        });
    }
    triggerConfAlert("Delete", "Delete reservation: " + ReservationId, deleteReservation)
  }

  const MyReservations = () => {
    const CardTemplate = ({ item, index }) => {
      return (
        <>
          {
            item === null ?
              <></>
              :
              <Card key={index} style={{ marginBottom: '1vh' }}>
                <CardContent>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <IconButton aria-label="Generate QR Code">
                      <QrCode color="primary"
                        onClick={() => triggerQrCodeDialog(item)} />
                    </IconButton>
                    <div style={{ marginRight: '2vh', marginLeft: '2vh' }}>
                      <Typography >
                        Reservation: <b>{item.ReservationId}</b>
                      </Typography>
                      <Typography >
                        Slot: <b>{item.ParkingSlotId}</b>
                      </Typography>
                      <Typography>
                        Date: <b>{item.ReservationDate}</b>
                      </Typography>
                      <Typography>
                        Was made: {item.ReservationMadeDateTime} by: {item.Login}
                      </Typography>
                    </div>
                    <IconButton aria-label="Delete" edge="end">
                      <DeleteForever
                        onClick={() => triggerDeleteReservation(item.ReservationId)}
                        color="error" />
                    </IconButton>
                  </div>
                </CardContent>
              </Card>
          }
        </>
      )
    }

    return (
      <>
        {
          showAllReservations ?
            <div style={{ margin: 'auto' }}>
              {myreservations.map((item, index) => (
                <CardTemplate item={item} index={index} />
              ))}
            </div>
            :
            (
              (myreservations.find(item => item.ReservationDate === formatDate(selectedDate))) ?
                <CardTemplate item={myreservations.find(item => item.ReservationDate === formatDate(selectedDate))} index={0} />
                :
                <Card key={0} style={{ marginBottom: '1vh' }}>
                  <CardContent>
                    <Typography>There is no reservation for {formatDate(selectedDate)}!</Typography>
                  </CardContent>
              </Card>
            )
        }
      </>
    )
  }


  const Calendar = () => {
    const handleDateChange = (date) => {
      setSelectedDate(date);
    };

    return (
      <div>
        <Typography variant="h6">
          Change date:
        </Typography>
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
      const newReservation = () => {
        request.sendRequestForNewReservation(userProfile.token, reservation)
          .then(() => {
            updateParkingSlots();
            updateMyReservations();
          });
      }
      triggerConfAlert(
        "Reserve",
        "Confirm reservation: " + reservation["reservation"]["ParkingSlotId"] + ", date: " + reservation["reservation"]["ReservationDate"],
        newReservation)
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
              height: "50vh",
              width: "50vh",
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
            <Typography>
              New reservation
            </Typography>
            <hr />
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

  const [isShowReservationOpen, setShowReservationOpen] = React.useState(false);

  const ShowReservationForm = () => {
    const handleOnClose = () => {
      setShowReservationOpen(false);
    }


    const performDeleteReservation = () => {

      const ReservationId = myreservations.find(item => item.ReservationDate === formatDate(selectedDate)).ReservationId;
      if (!ReservationId) {
        handleOnClose()
      }

      triggerDeleteReservation(ReservationId)
      handleOnClose()
    }

    const getReservationId = () => {
      const value = myreservations.find(item => item.ReservationDate === formatDate(selectedDate));
      if (value) {
        return value.ReservationId
      }
      else
        return ""
    }

    return (
      <>
        <Dialog
          open={isShowReservationOpen}
          onClose={handleOnClose}
          PaperProps={{
            className: "gradient-border",
            style: {
              height: "50vh",
              width: "50vh",
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
            <Typography>
              Reservation details
            </Typography>
            <hr />
          </DialogTitle>
          <Typography variant="h5">
            Reservation code
          </Typography>
          <Typography variant="h4">
            <b>{getReservationId()}</b>
          </Typography>
          <Typography variant="subtitle1">
            <b> slot number: {currentSlot === null ? "" : currentSlot.ParkingSlotId},</b>
          </Typography>
          <Typography variant="subtitle1">
            <b>location: {currentSlot === null ? "" : currentSlot.SlotNumber},</b>
          </Typography>
          <Typography variant="subtitle1">
            <b>floor: {currentSlot === null ? "" : currentSlot.Floor}</b>
          </Typography>
          <Typography variant="subtitle1">
            Reservation date: <b>{selectedDate === null ? "" : formatDate(selectedDate)}</b>
          </Typography>
          <Button
            onClick={performDeleteReservation}
            startIcon={<DeleteForever />}
            color="error"
            fullWidth
            sx={{ paddingBottom: "4vh", marginTop: "auto" }}
          >
            <b>Delete reservation</b>
          </Button>
        </Dialog>
      </>
    );
  };


  const ParkingSlots = () => {
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
        return false;
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
      setCurrentSlot(slot);
      setShowReservationOpen(true);
    }

    const openNewReservationForm = (slot) => {
      setCurrentSlot(slot);
      setNewReservationFormOpen(true);
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
                        <div ><b>{space.SlotNumber === '-1' ? <b>Entry</b> : space.ParkingSlotId}</b></div>
                        <div ><small>{space.SlotNumber === '-1' ? "" : space.isFree}</small></div>
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
        <hr style={{ width: '50%', margin: '0 auto', marginTop: "2vh", marginBottom: "2vh" }} />
        <div style={CENTER_STYLE}>
          <Button
            variant="contained"
            onClick={changeReservationCardView}
            endIcon={showAllReservations ? <Today /> : <CalendarMonth />}
            style={{ marginTop: "2vh", marginBottom: "2vh" }}>
            {showAllReservations ? "Show today reservation" : "Show all reservations"}
          </Button>
        </div>
        <div style={CENTER_STYLE}>
          <Typography variant='h6'>
            {showAllReservations ? "All reservations:" : "Reservation for " + formatDate(selectedDate) + ":"}
          </Typography>
        </div>
        <div style={CENTER_STYLE}>
          <MyReservations />
        </div>
        <hr style={{ width: '50%', margin: '0 auto', marginTop: "2vh", marginBottom: "2vh" }} />
        <div style={CENTER_STYLE}>
          <Calendar />
        </div>
        <div style={CENTER_STYLE}>
          <ParkingSlots />
        </div>
      </ContentBox >
      <NewReservationForm />
      <ShowReservationForm />
      <QrCodeDialog />
      <ConfirmationAlert />
    </>
  );

}
