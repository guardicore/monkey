'use client';
import AppBar from '@mui/material/AppBar';
import Container from '@mui/material/Container';
import Toolbar from '@mui/material/Toolbar';
import classes from './appBar.module.scss';
import React from 'react';
import AppMenu from '@/components/app-nav/app-menu/AppMenu';
import AppLogo from '@/components/app-nav/app-logo/AppLogo';
import Box from '@mui/material/Box';
import AppDrawerOpener from '@/components/app-nav/app-drawer-opener/AppDrawerOpener';
import useSmallScreenCheck from '@/hooks/useSmallScreenCheck';
import { ThemeMode } from '@/components/theme-mode/ThemeMode';

const buildMonkeyAppBar =
    (AppAvatar: React.ComponentType) =>
    // eslint-disable-next-line react/display-name
    ({ setIsDrawerOpen = null }: { setIsDrawerOpen: any }) => {
        const { screenIsSmall } = useSmallScreenCheck();

        return (
            <AppBar
                id={classes['app-bar']}
                position="static"
                color="primary"
                enableColorOnDark>
                <Container>
                    <Toolbar disableGutters>
                        <Box className="logo-and-menu-container">
                            <AppDrawerOpener
                                onClick={() => setIsDrawerOpen(true)}
                            />
                            <AppLogo />
                            {!screenIsSmall && <AppMenu />}
                        </Box>
                        <Box className="etc-container">
                            <ThemeMode />
                            <AppAvatar />
                        </Box>
                    </Toolbar>
                </Container>
            </AppBar>
        );
    };

export default buildMonkeyAppBar;
