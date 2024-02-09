import Box from '@mui/material/Box';
import React, { useState } from 'react';
import Tooltip from '@mui/material/Tooltip';
import IconButton from '@mui/material/IconButton';
import AccountCircle from '@mui/icons-material/AccountCircle';
import Menu from '@mui/material/Menu';
import AvatarMenu from '@/_components/app-nav/app-avatar/avatar-menu/AvatarMenu';
import { styled } from '@mui/material/styles';

const ThemedIcon = styled(AccountCircle)(({ theme }) => ({
    color: theme.palette.primary.contrastText
}));

const AppAvatar = (props) => {
    const [anchorElUser, setAnchorElUser] = useState<null | HTMLElement>(null);

    const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElUser(event.currentTarget);
    };

    const handleCloseUserMenu = () => {
        setAnchorElUser(null);
    };

    return (
        <Box {...props}>
            <Tooltip title="Open settings">
                <IconButton onClick={handleOpenUserMenu}>
                    <ThemedIcon className="profile-avatar" />
                </IconButton>
            </Tooltip>
            <Menu
                anchorEl={anchorElUser}
                keepMounted
                open={Boolean(anchorElUser)}
                onClose={handleCloseUserMenu}>
                <AvatarMenu />
            </Menu>
        </Box>
    );
};

export default AppAvatar;
