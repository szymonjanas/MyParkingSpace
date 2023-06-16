import * as React from 'react';
import { ContentBox } from '../ContextBox';
import { useProfile } from '../database/UserProfile';
import { Typography } from '@mui/material';
import DatePicker, { registerLocale, setDefaultLocale } from 'react-datepicker';
import Button from '@mui/material/Button';
import { useState } from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import pl from 'date-fns/locale/pl';
import { DUMMY_PARKING_SLOTS } from "../DummyParkingSlots"
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

    const isParkingSpaceMineAtCurrentDate = () =>
    {
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

    const showReservationForm = (slot) => {
      console.log("showReservationForm")

    }

    const newReservationForm = (slot) => {
      console.log("newReservationForm")
    }

    const onClickParkingSlotButtonAction = (slot) => 
    {
      if (isParkingSpaceMineAtCurrentDate())
        if (slot.isFree === "mine") {
          return showReservationForm(slot)
        }
      if (slot.isFree === "free") {
        return newReservationForm(slot)
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
    </>
  );

}
