import * as React from 'react';
import { getItemOrDefault, removeItem, setItem } from './Storage';

const PROFILE = {
    username: "",
    token: ""
}

export function useProfile() {
    const [userProfile, setUserProfile] = React.useState(() => getItemOrDefault("userProfile", PROFILE));

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
    }

    React.useEffect(() => {
        setItem('userProfile', userProfile);
    }, [userProfile]);

    return { userProfile, isLogin, login, logout }
}
