import React from 'react';
import RefreshIcon from '@mui/icons-material/Refresh';
import { spinningIcon } from '@/_components/icons/style';

type RefreshIconSpinningProps = {
    sx?: React.CSSProperties;
    isSpinning?: boolean;
};

const MonkeyRefreshIcon = (props: RefreshIconSpinningProps) => {
    if (props.isSpinning) {
        return <RefreshIcon {...props} sx={{ ...spinningIcon, ...props.sx }} />;
    } else {
        return <RefreshIcon {...props} sx={{ ...props.sx }} />;
    }
};

export default MonkeyRefreshIcon;
