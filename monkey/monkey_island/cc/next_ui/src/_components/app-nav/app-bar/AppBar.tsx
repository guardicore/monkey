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
import AppIconSvg from '@/assets/svg-components/AppIconSvg';
import useSmallScreenCheck from '@/hooks/useSmallScreenCheck';
import { PATHS } from '@/constants/paths.constants';
import { useRouter } from 'next/navigation';
import {
    appBar,
    appRouterLink,
    etcContainer,
    logoWrapper,
    logoAndDrawerContainer,
    logoAndMenuContainer,
    muiContainerRoot,
    muiToolbarRoot
} from '@/_components/app-nav/app-bar/style';

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
        <AppBar position="static" color="primary" enableColorOnDark sx={appBar}>
            <Container sx={muiContainerRoot}>
                <Toolbar disableGutters sx={muiToolbarRoot}>
                    <Box sx={logoAndMenuContainer}>
                        <Box sx={logoAndDrawerContainer}>
                            <AppDrawerOpener
                                onClick={() => setIsDrawerOpen(true)}
                            />
                            <SvgIcon
                                sx={logoWrapper}
                                onClick={() => handleRouteClick(PATHS.ROOT)}>
                                <AppIconSvg />
                            </SvgIcon>
                        </Box>
                        {!screenIsSmall && <AppMenu orientation="horizontal" />}
                    </Box>
                    <Box sx={etcContainer}>
                        <MenuItem
                            key={AboutLink.label}
                            sx={appRouterLink}
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
