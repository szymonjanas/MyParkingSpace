import * as React from 'react';
import { ContentBox } from './ContextBox';
import { useProfile } from './database/UserProfile';
import { Typography } from '@mui/material';
import DatePicker, { registerLocale, setDefaultLocale } from 'react-datepicker';
import Button from '@mui/material/Button';
import { useState } from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import pl from 'date-fns/locale/pl';
import { DUMMY_PARKING_SLOTS } from "./DummyParkingSlots"
registerLocale('pl', pl)
setDefaultLocale('pl')

const ParkingSpace = () => {


  const maxX = Math.max(...DUMMY_PARKING_SLOTS.map((space) => space.PositionX));
  const maxY = Math.max(...DUMMY_PARKING_SLOTS.map((space) => space.PositionY));

  const parking2D = new Array(maxY + 1).fill(null).map(() => new Array(maxX + 1).fill(null));

  DUMMY_PARKING_SLOTS.forEach((space) => {
    parking2D[space.PositionY][space.PositionX] = space;
  });

  return (
    <div>
      <table>
        <tbody>
          {parking2D.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((space, columnIndex) => (
                <td key={columnIndex}>
                  {space && (
                    <Button
                      variant="contained"
                      style={{ backgroundColor: space.isFree ? 'green' : 'grey', margin: 5 }}
                      disabled={!space.isFree}
                    >
                      {space.ParkingSlotId}
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

const MyCalendar = () => {
    const [selectedDate, setSelectedDate] = useState(new Date());
    
    const formatDate = (date) => {
      return date.toLocaleDateString('pl-PL', { day: '2-digit', month: '2-digit', year: 'numeric' });
    };
    
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

const CENTER_STYLE = {
    display: "flex",
    justifyContent: "center",
    alignItems: "center"
}

export function Home(){

    const { userProfile } = useProfile();


    return (
        <>
            <ContentBox>
                <Typography align="center">
                    Welcome <b>{userProfile.username}</b> in MyParkingSpace!
                </Typography>
            <div style={CENTER_STYLE}>
                <MyCalendar />
            </div>
            <div style={CENTER_STYLE}>
                <ParkingSpace />
            </div>
            </ContentBox>
        </>
    );

}
