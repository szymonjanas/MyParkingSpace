import * as React from 'react';
import { useState } from 'react';
import { Avatar, Button, Grid, IconButton, InputAdornment, Paper, TextField } from "@mui/material";
import LockIcon from '@mui/icons-material/Lock';
import { Login as LoginIcon, Visibility, VisibilityOff, GarageOutlined } from '@mui/icons-material';
import { sendRequestForLoginToServer, sendRequestForRegisterToServer } from './requests'
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

    const registerFormData = {
        emailRef: React.useRef(''),
        nameRef: React.useRef('')
    }

    const executeLoginRequest = () => {
        var loginValue = authFormData.loginRef.current.value;
        var passwordValue = authFormData.passwordRef.current.value;
        if (registration)
        {
            var emailValue = registerFormData.emailRef.current.value;
            var nameValue = registerFormData.nameRef.current.value;

            sendRequestForRegisterToServer(
                loginValue, passwordValue, emailValue, nameValue)
                .then((output) => {
                    if (output)
                        changeRegistrationForm(false)
                })

        }
        else
        {
            sendRequestForLoginToServer(loginValue, passwordValue)
                .then((token) => {
                    if (token && loginValue) {
                        login(token, loginValue);
                    }
                });
        }
    };

    const changeRegistrationForm = () => {
        setRegistration(!registration);
    }

    const [passwordVisible, setPasswordVisibility] = React.useState(false);
    const [registration, setRegistration] = useState(false);

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
                                <h2><GarageOutlined fontSize="large" style={{verticalAlign: "middle"}} /> MyParkingSpace</h2>
                                <hr />
                                <h3 style={{marginTop: "5vh"}}><Avatar><LockIcon /></Avatar> { registration ? "Sing up" : "Sign in" }</h3>
                                
                            </Grid>
                            { 
                                registration ? 
                                <>
                                    <TextField
                                        id='standard-basic'
                                        inputRef={ registration ? registerFormData.nameRef :  authFormData.nameRef}
                                        label='name'
                                        variant='standard'
                                        fullWidth
                                        required
                                        autoFocus
                                        autoComplete='true'
                                    />
                                    <TextField
                                        id='standard-basic'
                                        inputRef={ registration ? registerFormData.emailRef : authFormData.emailRef}
                                        label='email'
                                        variant='standard'
                                        fullWidth
                                        required
                                        autoFocus
                                        autoComplete='true'
                                    />
                                </> :
                                <></>
                            }
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
                                onKeyDown={onEnterKeyPressInPasswordField}
                            />
                            <Button
                                type='submit'
                                color='primary'
                                variant="contained"
                                style={{...btnStyle, marginBottom: "5vh" }}
                                fullWidth
                                onClick={executeLoginRequest}>
                                { registration ? "Register" : "Login" } 
                                <LoginIcon style={{ marginLeft: '1vh'}} />
                            </Button>
                            <hr />
                            <Button
                                onClick={changeRegistrationForm}
                                fullWidth>
                                { registration ? "Go to login" : "Go to registration" }
                            </Button>
                        </Paper>
                    </Grid>
                </>
            }
        </>
    )
}
