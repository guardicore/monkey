import Autorenew from '@mui/icons-material/Autorenew';
import React from 'react';
import { spinningIcon } from '@/_components/icons/style';

type LoadingIconProps = {
    sx?: React.CSSProperties;
};

const MonkeyLoadingIcon = (props: LoadingIconProps) => {
    return <Autorenew sx={{ ...spinningIcon, ...props.sx }} />;
};

export default MonkeyLoadingIcon;
