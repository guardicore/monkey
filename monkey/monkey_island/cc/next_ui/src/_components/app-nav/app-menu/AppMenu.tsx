import { PATHS } from '@/constants/paths.constants';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import React from 'react';
import { useRouter } from 'next/navigation';
import classes from './appMenu.module.scss';
import HomeIcon from '@mui/icons-material/Home';
import HubIcon from '@mui/icons-material/Hub';
import EventNoteIcon from '@mui/icons-material/EventNote';
import SettingsIcon from '@mui/icons-material/Settings';

const MenuLinks = [
    { path: PATHS.HOME, label: 'Home', icon: <HomeIcon /> },
    { path: PATHS.MAP, label: 'Map', icon: <HubIcon /> },
    { path: PATHS.EVENTS, label: 'Events', icon: <EventNoteIcon /> },
    {
        path: PATHS.CONFIGURATION,
        label: 'Configuration',
        icon: <SettingsIcon />
    }
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
