'use client';
import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import HomeIcon from '@mui/icons-material/Home';
import MenuItem from '@mui/material/MenuItem';
import SvgIcon from '@mui/material/SvgIcon';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import AppAvatar from '@/_components/app-nav/app-avatar/AppAvatar';
import AppDrawerOpener from '@/_components/app-nav/app-drawer-opener/AppDrawerOpener';
import AppMenu from '@/_components/app-nav/app-menu/AppMenu';
import MonkeyHeadSvg from '@/assets/svg-components/MonkeyHead.svg';
import useSmallScreenCheck from '@/hooks/useSmallScreenCheck';
import { PATHS } from '@/constants/paths.constants';
import { useRouter } from 'next/navigation';
import classes from './appBar.module.scss';

const AboutLink = { path: PATHS.ABOUT, label: 'About', icon: <HomeIcon /> };

export interface MenuProps {
    onClose?: () => void;
}

const MonkeyAppBar = (
    { setIsDrawerOpen = null }: { setIsDrawerOpen: any },
    { onClose }: MenuProps
) => {
    const { screenIsSmall } = useSmallScreenCheck();

    const router = useRouter();

    const handleRouteClick = (path: string) => {
        router.push(path);
        onClose && onClose();
    };

    return (
        <AppBar
            id={classes['app-bar']}
            position="static"
            color="primary"
            enableColorOnDark>
            <Container>
                <Toolbar disableGutters>
                    <Box className="logo-and-menu-container">
                        <Box className="logo-and-drawer-container">
                            <AppDrawerOpener
                                onClick={() => setIsDrawerOpen(true)}
                            />
                            <SvgIcon
                                className={'logo-icon'}
                                onClick={() => handleRouteClick(PATHS.ROOT)}>
                                <MonkeyHeadSvg />
                            </SvgIcon>
                        </Box>
                        {!screenIsSmall && <AppMenu orientation="horizontal" />}
                    </Box>
                    <Box className="etc-container">
                        <MenuItem
                            key={AboutLink.label}
                            className={'app-route-link'}
                            onClick={() => handleRouteClick(AboutLink.path)}>
                            <Typography>{AboutLink.label}</Typography>
                        </MenuItem>
                        <AppAvatar />
                    </Box>
                </Toolbar>
            </Container>
        </AppBar>
    );
};

export default MonkeyAppBar;
