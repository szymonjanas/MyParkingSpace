import * as React from 'react';
import { AppBar, Button, Container, Dialog, DialogTitle, Link, Toolbar, Typography } from "@mui/material";
import { AccountCircle, Logout } from '@mui/icons-material';
import { Box } from '@mui/system';
import { useScreenSize } from './screenSize';
import { useProfile } from './database/UserProfile';
import { ConfirmLogoutAlert } from './ConfirmLogoutAlert';


export function Topbar() {

    const { isMobile } = useScreenSize();
    const { userProfile } = useProfile();

    const [isUsernameForMobileDialogOpen, setUsernameForMobileDialog] = React.useState(false);

    const [confirmLogoutAlertStatus, setConfirmLogoutAlertStatus] = React.useState(false);
    const openlogoutAlert = () => setConfirmLogoutAlertStatus(true);
    const closelogoutAlert = () => setConfirmLogoutAlertStatus(false);

    const handleOpenUsernameForMobileDialog = () => {
        if (isMobile()) {
            setUsernameForMobileDialog(true);
        }
    }

    const handleCloseUsernameForMobileDialog = () => {
        setUsernameForMobileDialog(false);
    }

    return (
        <Box sx={{ display: 'flex' }}>
            <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
                <Container maxWidth="100%" >
                    <Toolbar disableGutters
                        style={{ display: "flex", justifyContent: "space-between" }}
                    >
                        {/* Logo and sidebar button */}
                        <Box
                            style={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center'
                            }}
                        >
                            <Typography
                                variant="h6"
                                noWrap
                                component="div"
                                style={{ float: "left" }}
                                sx={{ mr: 2 }}
                            >
                                <Link href={"/"} underline="none" color="inherit"> MyParkingSpace </Link>
                            </Typography>
                        </Box>

                        {/* Username and Logout button */}
                        <Box style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}>
                            <Typography
                                variant="h8"
                                style={{ float: "left" }}
                                sx={{ mr: 0, display: { xs: 'none', md: 'flex' } }}>
                                {userProfile.username}
                            </Typography>
                            <AccountCircle onClick={handleOpenUsernameForMobileDialog} style={{ marginLeft: '1vh', mr: 2 }} />

                            <Button
                                onClick={openlogoutAlert}
                                variant="contained"
                                style={{ marginLeft: "2vh" }}
                                color="secondary"
                                endIcon={<Logout />}>
                                <b>Logout</b>
                            </Button>
                        </Box>
                    </Toolbar>
                </Container>
            </AppBar>

            {/* Show username on Dialog when is mobile */}
            <Dialog
                onClose={handleCloseUsernameForMobileDialog}
                open={isUsernameForMobileDialogOpen}
            >
                <DialogTitle>{userProfile.username}</DialogTitle>
            </Dialog>

            <ConfirmLogoutAlert
                open={confirmLogoutAlertStatus}
                onClose={closelogoutAlert}
            />
        </Box>
    );
}