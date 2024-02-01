import { PATHS } from '@/constants/paths.constants';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import React from 'react';
import { useRouter } from 'next/navigation';
import classes from './appMenu.module.scss';
import HomeIcon from '@mui/icons-material/Home';
import HubIcon from '@mui/icons-material/Hub';

const MenuLinks = [
    { path: PATHS.CONFIGURE, label: 'Configure', icon: <HomeIcon /> },
    { path: PATHS.RUN, label: 'Run', icon: <HomeIcon /> },
    { path: PATHS.NETWORK_MAP, label: 'Network Map', icon: <HubIcon /> },
    { path: PATHS.REPORT, label: 'Report', icon: <HomeIcon /> }
];

export interface MenuProps {
    onClose?: () => void;
}

const AppMenu = ({ onClose }: MenuProps) => {
    const router = useRouter();

    const handleRouteClick = (path: string) => {
        router.push(path);
        onClose && onClose();
    };

    return (
        <Box className={classes['app-menu']}>
            <Box className="menu-links">
                {MenuLinks.map((link) => (
                    <div
                        key={link.label}
                        className={'app-route-link'}
                        onClick={() => handleRouteClick(link.path)}>
                        <Typography>{link.label}</Typography>
                    </div>
                ))}
            </Box>
        </Box>
    );
};

export default AppMenu;
