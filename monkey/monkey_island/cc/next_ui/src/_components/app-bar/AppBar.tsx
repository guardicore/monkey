'use client';
import AppBar from '@mui/material/AppBar';
import Container from '@mui/material/Container';
import Toolbar from '@mui/material/Toolbar';
import SvgIcon from '@mui/material/SvgIcon';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import MonkeyHeadSvg from '@/assets/svg-components/MonkeyHead.svg';
import MonkeyNameSvg from '@/assets/svg-components/MonkeyName.svg';
import classes from './appBar.module.scss';
import { useRouter } from 'next/navigation';
import { ALL_LINKS, AUTHENTICATED_PATHS } from '@/constants/paths.constants';
import Tooltip from '@mui/material/Tooltip';
import IconButton from '@mui/material/IconButton';
import Avatar from '@mui/material/Avatar';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import LogoutButton from '@/_components/logout-button/LogoutButton';
import React, { useState } from 'react';

const MonkeyAppBar = () => {
    const router = useRouter();

    const [anchorElUser, setAnchorElUser] = useState<null | HTMLElement>(null);

    const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElUser(event.currentTarget);
    };

    const handleCloseUserMenu = () => {
        setAnchorElUser(null);
    };

    const handleRouteClick = (path: string) => {
        router.push(path);
    };

    return (
        <AppBar
            id={classes['app-bar']}
            position="static"
            color="primary"
            enableColorOnDark>
            <Container maxWidth="xl">
                <Toolbar disableGutters>
                    <Box
                        className={'app-logo-container'}
                        onClick={() =>
                            handleRouteClick(AUTHENTICATED_PATHS.ROOT)
                        }>
                        <SvgIcon inheritViewBox={true}>
                            <MonkeyHeadSvg />
                        </SvgIcon>
                        <SvgIcon inheritViewBox={true}>
                            <MonkeyNameSvg />
                        </SvgIcon>
                    </Box>
                    <Box className={'app-links'}>
                        {ALL_LINKS.map((currPath) => (
                            <div
                                key={currPath.label}
                                className={'app-route-link'}
                                onClick={() => handleRouteClick(currPath.path)}>
                                <Typography>{currPath.label}</Typography>
                            </div>
                        ))}
                    </Box>
                    <Box className={'profile-wrapper'}>
                        <Tooltip title="Open settings">
                            <IconButton
                                onClick={handleOpenUserMenu}
                                sx={{ p: 0 }}>
                                <Avatar
                                    alt="Remy Sharp"
                                    src="/static/images/avatar/2.jpg"
                                />
                            </IconButton>
                        </Tooltip>
                        <Menu
                            sx={{ mt: '45px' }}
                            id="menu-appbar"
                            anchorEl={anchorElUser}
                            anchorOrigin={{
                                vertical: 'top',
                                horizontal: 'right'
                            }}
                            keepMounted
                            transformOrigin={{
                                vertical: 'top',
                                horizontal: 'right'
                            }}
                            open={Boolean(anchorElUser)}
                            onClose={handleCloseUserMenu}>
                            <MenuItem onClick={handleCloseUserMenu}>
                                <LogoutButton />
                            </MenuItem>
                        </Menu>
                    </Box>
                </Toolbar>
            </Container>
        </AppBar>
    );
};

export default MonkeyAppBar;
