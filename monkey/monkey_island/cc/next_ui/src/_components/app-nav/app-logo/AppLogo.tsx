import { AUTHENTICATED_ROOT_PATH } from '@/constants/paths.constants';
import Box from '@mui/material/Box';
import React from 'react';
import { useRouter } from 'next/navigation';
import SvgIcon from '@mui/material/SvgIcon';
import MonkeyHeadSvg from '@/assets/svg-components/MonkeyHead.svg';
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
            onClick={() => handleLogoClick(AUTHENTICATED_ROOT_PATH)}>
            <SvgIcon inheritViewBox={true} className={'logo-icon'}>
                <MonkeyHeadSvg />
            </SvgIcon>
            <SvgIcon inheritViewBox={true} className={'logo-text'}>
                <MonkeyNameSvg />
            </SvgIcon>
        </Box>
    );
};

export default AppLogo;
