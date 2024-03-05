import React, { useState } from 'react';
import Zoom from '@mui/material/Zoom';
import { Tooltip, TooltipProps } from '@mui/material';
import { tooltipStyle, tooltipTextStyle } from '@/_components/tooltips/style';
import Box from '@mui/material/Box';

export enum TooltipPlacement {
    TOP = 'top',
    BOTTOM = 'bottom',
    LEFT = 'left',
    RIGHT = 'right'
}

type MonkeyTooltipProps = TooltipProps & {
    placement?: TooltipProps['placement'];
    isOverflow?: boolean;
    children?: any;
};

const MonkeyTooltip = (props: MonkeyTooltipProps) => {
    const {
        placement = undefined,
        isOverflow = false,
        children = [],
        ...rest
    } = { ...props };

    const [tooltipEnabled, setTooltipEnabled] = useState(false);

    const handleShouldShow = ({ currentTarget }) => {
        if (currentTarget.scrollWidth > currentTarget.clientWidth) {
            setTooltipEnabled(true);
        }
    };

    const forwardedProps = Object.assign(
        { ...rest },
        {
            placement: placement || TooltipPlacement.TOP,
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
