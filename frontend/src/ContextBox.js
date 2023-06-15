import * as React from 'react';
import { Box } from '@mui/material';
import { useScreenSize } from './screenSize';

export const ContentBoxStyle_Mobile = {
    mt: 10, 
    ml: 2, 
    mr: 2, 
    mb: 0, 
    padding: 0
};

export const ContentBoxStyle_Desktop = {
    mt: 10, 
    ml: (10 + "px"), 
    mr: "10px", 
    mb: 0, 
    padding: 0
}

export function ContentBox(props) {

    const { isMobile } = useScreenSize();
    
    return (
        <Box sx={isMobile() ? ContentBoxStyle_Mobile : ContentBoxStyle_Desktop}>
            {props.children}
        </Box>
    );
}
