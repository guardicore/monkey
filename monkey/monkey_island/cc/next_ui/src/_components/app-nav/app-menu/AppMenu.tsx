import { PATHS } from '@/constants/paths.constants';
import React from 'react';
import { usePathname, useRouter } from 'next/navigation';
import HomeIcon from '@mui/icons-material/Home';
import HubIcon from '@mui/icons-material/Hub';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';

const MenuLinks = [
    { path: PATHS.CONFIGURE, label: 'Configure', icon: <HomeIcon /> },
    { path: PATHS.RUN, label: 'Run', icon: <HomeIcon /> },
    { path: PATHS.NETWORK_MAP, label: 'Network Map', icon: <HubIcon /> },
    { path: PATHS.REPORT, label: 'Report', icon: <HomeIcon /> }
];

export interface MenuProps {
    onClose?: () => void;
    orientation?: 'vertical' | 'horizontal';
}

const AppMenu = ({ orientation, onClose }: MenuProps) => {
    const router = useRouter();
    const path = usePathname();

    const handleRouteClick = (event: React.SyntheticEvent, value: any) => {
        router.push(value);
        onClose && onClose();
    };

    return (
        <Tabs
            orientation={orientation}
            value={path}
            className="menu-links"
            onChange={handleRouteClick}
            textColor="inherit"
            indicatorColor="secondary">
            {MenuLinks.map((link) => (
                <Tab
                    key={link.label}
                    className={'app-route-link'}
                    label={link.label}
                    value={link.path}
                />
            ))}
        </Tabs>
    );
};

export default AppMenu;
