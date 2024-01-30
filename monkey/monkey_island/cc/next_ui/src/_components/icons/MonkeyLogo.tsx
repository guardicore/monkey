import MonkeyHeadSvg from '@/assets/svg-components/MonkeyHead.svg';
import MonkeNameSvg from '@/assets/svg-components/MonkeyName.svg';
import Stack from '@mui/material/Stack';

import classes from './MonkeyLogo.module.scss';

const MonkeyLogo = (props) => {
    return (
        <Stack
            className={classes.monkeyLogo}
            direction="row"
            useFlexGap
            {...props}>
            <MonkeyHeadSvg className={classes.logo} color={props.color} />
            <MonkeNameSvg className={classes.name} color={props.color} />
        </Stack>
    );
};

export default MonkeyLogo;
