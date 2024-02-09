import { PATHS } from '@/constants/paths.constants';
import React from 'react';
import { usePathname, useRouter } from 'next/navigation';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import useSmallScreenCheck from '@/hooks/useSmallScreenCheck';

const MenuLinksLeft = [
    { path: PATHS.CONFIGURE, label: 'Configure' },
    { path: PATHS.RUN, label: 'Run' },
    { path: PATHS.NETWORK_MAP, label: 'Network Map' },
    { path: PATHS.REPORT, label: 'Report' }
];

const MenuLinksRight = [{ path: PATHS.ABOUT, label: 'About' }];

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
    const { screenIsSmall } = useSmallScreenCheck();

    const handleRouteClick = (event: React.SyntheticEvent, value: any) => {
        router.push(value);
        onClose && onClose();
    };

    return (
        <Tabs
            orientation={orientation}
            value={getTabValue(path)}
            onChange={handleRouteClick}
            textColor="inherit"
            indicatorColor="secondary"
            sx={{ width: '100%' }}>
            {MenuLinksLeft.map((link) => (
                <Tab key={link.label} label={link.label} value={link.path} />
            ))}
            {MenuLinksRight.map((link, index) => (
                <Tab
                    key={link.label}
                    label={link.label}
                    value={link.path}
                    sx={index === 0 && !screenIsSmall ? { ml: 'auto' } : {}}
                />
            ))}
        </Tabs>
    );
};

export default AppMenu;
