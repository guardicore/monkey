import Autorenew from '@mui/icons-material/Autorenew';
import React from 'react';
import { loadingIcon } from '@/_components/icons/loading-icon/style';

const LoadingIcon = (props) => {
    return <Autorenew {...props} sx={{ ...loadingIcon, ...props.sx }} />;
};

export default LoadingIcon;
