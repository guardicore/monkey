import { AUTHENTICATED_PATHS } from '@/constants/paths.constants';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import React from 'react';
import { useRouter } from 'next/navigation';
import classes from './appMenu.module.scss';

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
                {AUTHENTICATED_PATHS.map((currPath) => (
                    <div
                        key={currPath.label}
                        className={'app-route-link'}
                        onClick={() => handleRouteClick(currPath.path)}>
                        <Typography>{currPath.label}</Typography>
                    </div>
                ))}
            </Box>
        </Box>
    );
};

export default AppMenu;
