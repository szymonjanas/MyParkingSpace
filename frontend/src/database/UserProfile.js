import * as React from 'react';
import { getItemOrDefault, removeItem, setItem } from './Storage';
import { sendRequestForUserInfo } from '../requests';

const PROFILE = {
    username: "",
    token: ""
}

const DETAILS = {
    RegistrationDate: "",
    Name: "",
    Login: "",
    Email: ""
}

export function useProfile() {
    const [userProfile, setUserProfile] = React.useState(() => getItemOrDefault("userProfile", PROFILE));
    const [userDetails, setUserInfo] = React.useState(() => getItemOrDefault("userDetails", DETAILS));
    function login(token, username) {
        if (Boolean(username) === false &&
            Boolean(token) === false) {
            removeItem("userProfile");
        } else {
            setUserProfile({
                username: username,
                token: token
            })
        }
    }

    function isLogin() {
        return Boolean(userProfile.username) && Boolean(userProfile.token);
    }

    function logout() {
        removeItem("userProfile");
        removeItem("userDetails");
    }

    function setUserDetails() {
        if (userProfile.token !== "")
            sendRequestForUserInfo(userProfile.token)
                .then((userDetails) => {
                    setUserInfo(userDetails)
                    console.log(userDetails)
                });
    }

    React.useEffect(() => {
        setItem('userProfile', userProfile);
        setUserDetails()
    }, [userProfile]);

    React.useEffect(() => {
        setItem('userDetails', userDetails);
    }, [userDetails]);

    return { userProfile, isLogin, login, logout, userDetails }
}
