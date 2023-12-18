import { ROUTES } from '@/constants/paths.constants';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import React from 'react';
import { useRouter } from 'next/navigation';
import classes from './appMenu.module.scss';
import HomeIcon from '@mui/icons-material/Home';
import HubIcon from '@mui/icons-material/Hub';
import EventNoteIcon from '@mui/icons-material/EventNote';

const MenuLinks = [
    { path: ROUTES.HOME, label: 'Home', icon: <HomeIcon /> },
    { path: ROUTES.MAP, label: 'Map', icon: <HubIcon /> },
    { path: ROUTES.EVENTS, label: 'Events', icon: <EventNoteIcon /> }
];

const AppMenu = ({ onClose }: { onClose?: object }) => {
    const router = useRouter();

    const handleRouteClick = (path: string) => {
        router.push(path);
        // @ts-ignore
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
