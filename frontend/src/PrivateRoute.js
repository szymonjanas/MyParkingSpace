import * as React from 'react';
import { Navigate } from 'react-router-dom';
import { useProfile } from './database/UserProfile';

export function PrivateRoute({ children }) {

    const { isLogin } = useProfile();

    return (
        isLogin() ? children : <Navigate to='/login' />
    );
}
