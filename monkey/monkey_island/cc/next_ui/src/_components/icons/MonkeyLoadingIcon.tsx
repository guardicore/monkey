import Autorenew from '@mui/icons-material/Autorenew';
import React from 'react';
import { spinningIcon } from '@/_components/icons/style';
import { SxProps } from '@mui/material';

type LoadingIconProps = {
    sx?: SxProps;
};

const MonkeyLoadingIcon = (props: LoadingIconProps) => {
    return <Autorenew sx={{ ...spinningIcon, ...props.sx }} />;
};

export default MonkeyLoadingIcon;
