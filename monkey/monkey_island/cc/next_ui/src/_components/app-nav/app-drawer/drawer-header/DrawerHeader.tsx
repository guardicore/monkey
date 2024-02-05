import Box from '@mui/material/Box';
import CloseIcon from '@mui/icons-material/Close';
import classes from './drawerHeader.module.scss';
import IconButton from '@mui/material/IconButton';
import MonkeyHeadSvg from '@/assets/svg-components/MonkeyHead.svg';
import SvgIcon from '@mui/material/SvgIcon';
import React from 'react';
import { styled } from '@mui/material/styles';

export interface DrawerHeaderProps {
    onClose?: () => void;
}

const ThemedCloseIcon = styled(CloseIcon)(({ theme }) => ({
    color: theme.palette.primary.contrastText
}));

const DrawerHeaderStyled = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText
}));

const DrawerHeader = ({ onClose }: DrawerHeaderProps) => {
    const handleDrawerClose = () => {
        onClose && onClose();
    };

    return (
        <DrawerHeaderStyled id={classes['app-drawer-header']}>
            <Box className="logo-icon-wrapper">
                <SvgIcon inheritViewBox={true} className={'logo-icon'}>
                    <MonkeyHeadSvg />
                </SvgIcon>
            </Box>
            <Box className="drawer-header-close">
                <IconButton onClick={handleDrawerClose} size="small">
                    <ThemedCloseIcon />
                </IconButton>
            </Box>
        </DrawerHeaderStyled>
    );
};

export default DrawerHeader;
