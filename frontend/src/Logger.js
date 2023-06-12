import * as React from 'react';
import { Alert, IconButton, Snackbar } from "@mui/material";
import { Close } from '@mui/icons-material';

export const LOGGER_TYPE = {
    ERROR: "error",
    WARNING: "warning",
    INFO: "info",
    SUCCESS: "success"
};

export const LOGGER_MESSAGE = {
    TYPE: LOGGER_TYPE.INFO,
    MESSAGE: "LOGGER MESSAGE"
};

export function logMessage(type = LOGGER_TYPE.INFO, message = "LOGGER_MESSAGE") {
    var msg = LOGGER_MESSAGE;
    msg.TYPE = type;
    msg.MESSAGE = message;

    const customEvent = new CustomEvent("logMessage", {
        detail: msg
    });
    document.dispatchEvent(customEvent);
};

export function Logger({
    autoHideDuration = 6000 }) {

    const [logMessage, setLogMessage] = React.useState(LOGGER_MESSAGE);
    const [open, setOpen] = React.useState(false);

    document.addEventListener("logMessage", function ({ detail }) {
        setLogMessage(detail);
        console.log(detail);
        setOpen(true);
    });

    const onClose = () => {
        setOpen(false);
    };

    return (
        <Snackbar
            open={open}
            autoHideDuration={autoHideDuration}
            onClose={onClose}>
            <Alert
                action={
                    <IconButton
                        aria-label="close"
                        color="inherit"
                        size="small"
                        onClick={onClose}
                    >
                        <Close fontSize="inherit" />
                    </IconButton>}
                severity={logMessage.TYPE}
                sx={{ width: '100%' }}>
                {logMessage.MESSAGE}
            </Alert>
        </Snackbar>
    );
}
