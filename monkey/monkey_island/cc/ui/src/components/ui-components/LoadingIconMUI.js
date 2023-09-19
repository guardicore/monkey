import Autorenew from '@mui/icons-material/Autorenew';
import React from 'react';

function LoadingIcon(props) {
  return <Autorenew {...props}
    sx = {{
      animation: 'spin-animation 0.5s infinite',
      display: 'inline-block'
    }}
  />
}

export default LoadingIcon;
