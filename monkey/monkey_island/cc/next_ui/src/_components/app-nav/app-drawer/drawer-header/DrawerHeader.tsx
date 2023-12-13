import Box from '@mui/material/Box';
import CloseIcon from '@mui/icons-material/Close';
import classes from './drawerHeader.module.scss';
import IconButton from '@mui/material/IconButton';
import MonkeyHeadSvg from '@/assets/svg-components/MonkeyHead.svg';
import SvgIcon from '@mui/material/SvgIcon';
import React from 'react';

const DrawerHeader = ({ onClose }: { onClose: object }) => {
    const handleDrawerClose = () => {
        // @ts-ignore
        onClose && onClose();
    };

    return (
        <Box id={classes['app-drawer-header']}>
            <Box className="logo-icon-wrapper">
                <SvgIcon inheritViewBox={true} className={'logo-icon'}>
                    <MonkeyHeadSvg />
                </SvgIcon>
            </Box>
            <Box className="drawer-header-close">
                <IconButton onClick={handleDrawerClose} size="small">
                    <CloseIcon />
                </IconButton>
            </Box>
        </Box>
    );
};

export default DrawerHeader;
