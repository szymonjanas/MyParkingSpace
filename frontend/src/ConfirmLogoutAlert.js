import * as React from 'react';
import { Button, Dialog, DialogActions, DialogTitle } from '@mui/material';
import { useProfile } from './database/UserProfile';
import { sendRequestForLogoutToServer } from './requests';

export function ConfirmLogoutAlert(props) {

  const { userProfile, logout } = useProfile();

  const handleClose = () => {
    props.onClose();
  };

  const handleLogout = () => {
    sendRequestForLogoutToServer(userProfile.token)
      .then((output) => {
          if (output) {
            logout();
            handleClose();
          }
      })
  };

  return (
    <>
      <Dialog
        open={props.open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >

        <DialogTitle id="alert-dialog-title">
          Please, confirm logout
        </DialogTitle>
        <DialogActions style={{ display: 'flex', justifyContent: 'center' }}>
          <Button onClick={handleClose} autoFocus>
            Cancel
          </Button>
          <Button onClick={handleLogout} href="/" style={{ marginLeft: '2vh' }} >
            Logout
          </Button>
        </DialogActions>

      </Dialog>
    </>
  );
}
