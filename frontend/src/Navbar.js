import * as React from 'react';
import { Topbar } from './Topbar';
import { Outlet } from 'react-router-dom';

export function Navbar() {

    return (
        <>
            <Outlet />
            <Topbar/>
        </>
    );
}
