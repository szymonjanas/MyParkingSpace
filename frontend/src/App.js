import * as React from 'react';
import { createTheme, CssBaseline, ThemeProvider } from '@mui/material';
import { Logger } from './Logger';
import { Routes, Route } from 'react-router-dom';
import { PrivateRoute } from './PrivateRoute';

const theme = createTheme({
  palette: {
    mode: 'light',
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Logger />
      <Routes>
        {/* <Route path="login" element={<Login />} /> */}
        <Route path="/" element={
          <PrivateRoute>
            {/* <Navbar /> */}
          </PrivateRoute>
        }>
          {/* <Route index path="/" element={<Home />} /> */}
        </Route>
      </Routes>
    </ThemeProvider>
  );
}

export default App;
