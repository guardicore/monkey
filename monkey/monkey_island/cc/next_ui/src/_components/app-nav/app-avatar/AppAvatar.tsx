import Box from '@mui/material/Box';
import React, { useState } from 'react';
import Tooltip from '@mui/material/Tooltip';
import IconButton from '@mui/material/IconButton';
import Avatar from '@mui/material/Avatar';
import Menu from '@mui/material/Menu';
import AvatarMenu from '@/_components/app-nav/app-avatar/avatar-menu/AvatarMenu';

const AVATAR_INITIALS = 'M';

const AppAvatar = () => {
    const [anchorElUser, setAnchorElUser] = useState<null | HTMLElement>(null);

    const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElUser(event.currentTarget);
    };

    const handleCloseUserMenu = () => {
        setAnchorElUser(null);
    };

    return (
        <Box id={'app-avatar'}>
            <Tooltip title="Open settings">
                <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                    <Avatar alt="Monkey Head">{AVATAR_INITIALS}</Avatar>
                </IconButton>
            </Tooltip>
            <Menu
                sx={{ mt: '40px' }}
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
                <AvatarMenu />
            </Menu>
        </Box>
    );
};

export default AppAvatar;
