import React, { useState } from 'react';
import Zoom from '@mui/material/Zoom';
import { Tooltip } from '@mui/material';
import { tooltipStyle, tooltipTextStyle } from '@/_components/tooltips/style';
import Box from '@mui/material/Box';

export const TOOLTIP_POSITION = {
    TOP: 'top',
    BOTTOM: 'bottom',
    LEFT: 'left',
    RIGHT: 'right'
};

const MonkeyTooltip = (props) => {
    const { placement, isOverflow = false, children, ...rest } = { ...props };

    const [tooltipEnabled, setTooltipEnabled] = useState(false);

    const handleShouldShow = ({ currentTarget }) => {
        if (currentTarget.scrollWidth > currentTarget.clientWidth) {
            setTooltipEnabled(true);
        }
    };

    const forwardedProps = Object.assign(
        { ...rest },
        {
            placement: placement || TOOLTIP_POSITION.TOP,
            TransitionComponent: Zoom
        }
    );

    if (isOverflow) {
        return (
            <Tooltip
                {...forwardedProps}
                arrow
                open={tooltipEnabled}
                sx={tooltipStyle}>
                <Box
                    sx={tooltipTextStyle}
                    onMouseEnter={handleShouldShow}
                    onMouseLeave={() => setTooltipEnabled(false)}>
                    {children}
                </Box>
            </Tooltip>
        );
    }

    return (
        <Tooltip {...forwardedProps} arrow>
            {children}
        </Tooltip>
    );
};

export default MonkeyTooltip;
