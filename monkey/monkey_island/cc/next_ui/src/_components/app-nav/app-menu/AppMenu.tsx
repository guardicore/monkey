import { PATHS } from '@/constants/paths.constants';
import React from 'react';
import { usePathname, useRouter } from 'next/navigation';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';

const MenuLinks = [
    { path: PATHS.CONFIGURE, label: 'Configure' },
    { path: PATHS.RUN, label: 'Run' },
    { path: PATHS.NETWORK_MAP, label: 'Network Map' },
    { path: PATHS.REPORT, label: 'Report' }
];

export interface MenuProps {
    onClose?: () => void;
    orientation?: 'vertical' | 'horizontal';
}

const getTabValue = (path) => {
    if (path === PATHS.ROOT) {
        return false;
    } else {
        return path;
    }
};

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
            value={getTabValue(path)}
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
