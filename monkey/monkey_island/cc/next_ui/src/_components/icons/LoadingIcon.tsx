import Autorenew from '@mui/icons-material/Autorenew';
import React from 'react';
import classes from './LoadingIcon.module.scss';

const LoadingIcon = (props) => {
    return <Autorenew {...props} id={classes['loading-icon']} />;
};

export default LoadingIcon;
