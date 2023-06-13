import * as React from 'react';
import { Avatar, Button, Grid, IconButton, InputAdornment, Paper, TextField } from "@mui/material";
import LockIcon from '@mui/icons-material/Lock';
import { Login as LoginIcon, Visibility, VisibilityOff } from '@mui/icons-material';
import { sendRequestForLoginToServer } from './requests'
import { Navigate } from 'react-router';
import { useProfile } from './database/UserProfile';

export function Login() {

    // ---------- STYLES ----------
    const paperStyle = {
        padding: 30,
        height: '100%',
        width: '100%',
        maxWidth: 300,
        margin: '6vh auto',
    }

    const btnStyle = {
        margin: '8px 0',
        marginTop: '6vh'
    }

    // ---------- AUTH FORM ----------
    const { isLogin, login } = useProfile();

    const authFormData = {
        loginRef: React.useRef(''),
        passwordRef: React.useRef('')
    }

    const executeLoginRequest = () => {
        var login = authFormData.loginRef.current.value;
        var password = authFormData.passwordRef.current.value;
        sendRequestForLoginToServer({ login, password })
            .then((token) => {
                if (token && login) {
                    login(token, login);
                }
            });
    };

    const [passwordVisible, setPasswordVisibility] = React.useState(false);

    const togglePasswordVisiblity = () => setPasswordVisibility(!passwordVisible);

    const onEnterKeyPressInPasswordField = (event) => {
        if (event.key === 'Enter') {
            executeLoginRequest();
        }
    };

    return (
        <>
            {isLogin() ?
                <Navigate to={"/"} /> :
                <>
                    <Grid>
                        <Paper elevation={10} style={paperStyle}>
                            <Grid align='center'>
                                <Avatar><LockIcon /></Avatar>
                                <h2>Sign in</h2>
                            </Grid>
                            <TextField
                                id='standard-basic'
                                inputRef={authFormData.loginRef}
                                label='login'
                                variant='standard'
                                fullWidth
                                required
                                autoFocus
                                autoComplete='true'
                            />
                            <TextField
                                id='outlined-password-input'
                                inputRef={authFormData.passwordRef}
                                label='password'
                                type={passwordVisible ? 'text' : 'password'}
                                variant='standard'
                                autoComplete="current-password"
                                fullWidth
                                required
                                InputProps={{
                                    endAdornment: (
                                        <InputAdornment position="end">
                                            <IconButton
                                                aria-label="toggle password visibility"
                                                onClick={togglePasswordVisiblity}>
                                                {passwordVisible ? <VisibilityOff /> : <Visibility />}
                                            </IconButton>
                                        </InputAdornment>
                                    )
                                }}
                                onKeyPress={onEnterKeyPressInPasswordField}
                            />
                            <Button
                                type='submit'
                                color='primary'
                                variant="contained"
                                style={btnStyle}
                                fullWidth
                                onClick={executeLoginRequest}>
                                Login
                                <LoginIcon style={{ marginLeft: '1vh' }} />
                            </Button>
                        </Paper>
                    </Grid>
                </>
            }
        </>
    )
}
