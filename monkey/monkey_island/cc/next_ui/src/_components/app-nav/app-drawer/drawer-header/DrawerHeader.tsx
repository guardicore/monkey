import Box from '@mui/material/Box';
import CloseIcon from '@mui/icons-material/Close';
import IconButton from '@mui/material/IconButton';
import MonkeyHeadSvg from '@/assets/svg-components/MonkeyHead.svg';
import SvgIcon from '@mui/material/SvgIcon';
import React from 'react';
import { styled } from '@mui/material/styles';
import {
    drawerHeader,
    logoIcon,
    logoWrapper
} from '@/_components/app-nav/app-drawer/drawer-header/style';

export interface DrawerHeaderProps {
    onClose?: () => void;
}

const DrawerHeaderStyled = styled('div')(({ theme }) => drawerHeader(theme));

const DrawerHeader = ({ onClose }: DrawerHeaderProps) => {
    const handleDrawerClose = () => {
        onClose && onClose();
    };

    return (
        <DrawerHeaderStyled>
            <Box sx={logoWrapper}>
                <SvgIcon inheritViewBox={true} sx={logoIcon}>
                    <MonkeyHeadSvg />
                </SvgIcon>
            </Box>
            <Box>
                <IconButton onClick={handleDrawerClose} size="small">
                    <CloseIcon sx={{ color: 'primary.contrastText' }} />
                </IconButton>
            </Box>
        </DrawerHeaderStyled>
    );
};

export default DrawerHeader;
