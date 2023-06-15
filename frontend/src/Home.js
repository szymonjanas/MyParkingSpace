import * as React from 'react';
import { ContentBox } from './ContextBox';
import { useProfile } from './database/UserProfile';
import { Typography } from '@mui/material';

export function Home(){

    const { userProfile } = useProfile();





    return (
        <>
            <ContentBox>
                <Typography align="center">
                    Welcome <b>{userProfile.username}</b> in MyParkingSpace!
                </Typography>
            </ContentBox>
        </>
    );

}
