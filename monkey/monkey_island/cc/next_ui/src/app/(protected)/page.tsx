'use client';
import GettingStarted from '@/_components/getting-started/GettingStarted';
import { appRootDiv } from './style';
import { styled } from '@mui/material/styles';

export default function AppHome() {
    // @ts-ignore
    const AppRootDiv = styled('div')(appRootDiv);
    return (
        <AppRootDiv>
            <GettingStarted />
        </AppRootDiv>
    );
}
