import * as React from 'react';
import { getItemOrDefault, removeItem, setItem } from './Storage';

const PROFILE = {
    username: "",
    jwt: ""
}

export function useProfile() {
    const [userProfile, setUserProfile] = React.useState(() => getItemOrDefault("userProfile", PROFILE));

    function login(jwt, username) {
        if (Boolean(username) === false &&
            Boolean(jwt) === false) {
            removeItem("userProfile");
        } else {
            setUserProfile({
                username: username,
                jwt: jwt
            })
        }
    }

    function isLogin() {
        return Boolean(userProfile.username) && Boolean(userProfile.jwt);
    }

    function logout() {
        removeItem("userProfile");
    }

    React.useEffect(() => {
        setItem('userProfile', userProfile);
    }, [userProfile]);

    return { userProfile, isLogin, login, logout }
}
