import { PATHS } from '@/constants/paths.constants';
import React from 'react';
import { useRouter } from 'next/navigation';
import MonkeyLogo from '@/_components/icons/monkey-logo/MonkeyLogo';
import classes from './appLogo.module.scss';

const AppLogo = () => {
    const router = useRouter();

    const handleLogoClick = (path: string) => {
        router.push(path);
    };

    return (
        <MonkeyLogo
            id={classes['app-logo']}
            onClick={() => handleLogoClick(PATHS.ROOT)}
        />
    );
};

export default AppLogo;
