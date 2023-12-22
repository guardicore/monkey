import React, {useState} from 'react';
import Zoom from '@mui/material/Zoom';
import {Tooltip} from '@mui/material';

export const TOOLTIP_POSITION = {
  TOP: 'top',
  BOTTOM: 'bottom',
  LEFT: 'left',
  RIGHT: 'right'
};

/*
  The CSS is located inside App.css ('.MuiTooltip-tooltip') as the tooltip is a global component which is appended
   on the body element.
*/

//* MonkeyTooltip is a wrapper for the Tooltip component from @mui/material.
//* It is used to set default values for the Tooltip component.
//* props are forwarded to the Tooltip component.
//* props can be overridden by passing them to the MonkeyTooltip component.
//* props are: title, placement, className, key, isOverflow.
//* The 'isOverflow' prop is meant to used in textual nodes only
const MonkeyTooltip = (props) => {
  const {placement, isOverflow = false, children, ...rest} = {...props};

  const [tooltipEnabled, setTooltipEnabled] = useState(false);

  const handleShouldShow = ({currentTarget}) => {
    if (currentTarget.scrollWidth > currentTarget.clientWidth) {
      setTooltipEnabled(true);
    }
  };

  const forwardedProps = Object.assign(
    {...rest},
    {
      placement: placement || TOOLTIP_POSITION.TOP,
      TransitionComponent: Zoom
    }
  );

  if (isOverflow) {
    return (
      <Tooltip {...forwardedProps}
               arrow
               open={tooltipEnabled}>
        <div className="text-truncate" onMouseEnter={handleShouldShow} onMouseLeave={()=> setTooltipEnabled(false)}>
          {children}
        </div>
      </Tooltip>
    )
  }

  return <Tooltip {...forwardedProps} arrow>{children}</Tooltip>;
};

export default MonkeyTooltip;
