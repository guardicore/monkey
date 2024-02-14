import { PATHS } from '@/constants/paths.constants';
import React from 'react';
import { useRouter, useSelectedLayoutSegments } from 'next/navigation';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import useSmallScreenCheck from '@/hooks/useSmallScreenCheck';
import { appTabsContainer } from '@/_components/app-nav/app-menu/style';

const MenuLinksLeft = [
    { path: PATHS.CONFIGURE, label: 'Configure' },
    { path: PATHS.RUN, label: 'Run' },
    { path: PATHS.NETWORK_MAP, label: 'Network Map' },
    { path: PATHS.REPORT, label: 'Report' },
    { path: PATHS.PLUGINS, label: 'Plugins' }
];

const MenuLinksRight = [{ path: PATHS.ABOUT, label: 'About' }];

export interface MenuProps {
    onClose?: () => void;
    orientation?: 'vertical' | 'horizontal';
}

const getTabValue = (segments) => {
    if (segments.length === 0) {
        return false;
    } else {
        return '/' + segments[0];
    }
};

const AppMenu = ({ orientation, onClose }: MenuProps) => {
    const router = useRouter();
    const { screenIsSmall } = useSmallScreenCheck();
    const urlSegments = useSelectedLayoutSegments();

    const handleRouteClick = (event: React.SyntheticEvent, value: any) => {
        router.push(value);
        onClose && onClose();
    };

    return (
        <Tabs
            orientation={orientation}
            value={getTabValue(urlSegments)}
            onChange={handleRouteClick}
            textColor="inherit"
            indicatorColor="secondary"
            sx={appTabsContainer}>
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
