import { PATHS } from '@/constants/paths.constants';
import Box from '@mui/material/Box';
import React from 'react';
import { useRouter } from 'next/navigation';
import SvgIcon from '@mui/material/SvgIcon';
import MonkeyIconSvg from '@/assets/svg-components/MonkeyIconSvg';
import MonkeyNameSvg from '@/assets/svg-components/MonkeyName.svg';
import classes from './appLogo.module.scss';

const AppLogo = () => {
    const router = useRouter();

    const handleLogoClick = (path: string) => {
        router.push(path);
    };

    return (
        <Box
            id={classes['app-logo']}
            onClick={() => handleLogoClick(PATHS.ROOT)}>
            <SvgIcon inheritViewBox={true} className={'logo-icon'}>
                <MonkeyIconSvg />
            </SvgIcon>
            <SvgIcon inheritViewBox={true} className={'logo-text'}>
                <MonkeyNameSvg />
            </SvgIcon>
        </Box>
    );
};

export default AppLogo;
