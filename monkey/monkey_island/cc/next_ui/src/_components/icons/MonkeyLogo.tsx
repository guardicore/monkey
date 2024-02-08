import MonkeyHeadSvg from '@/assets/svg-components/MonkeyHead.svg';
import MonkeNameSvg from '@/assets/svg-components/MonkeyName.svg';
import Stack from '@mui/material/Stack';

import classes from './MonkeyLogo.module.scss';
import { useTheme } from '@mui/material/styles';

const MonkeyLogo = (props) => {
    const theme = useTheme();
    const color = props.color || theme.palette.primary.main;

    return (
        <Stack
            className={classes.monkeyLogo}
            direction="row"
            useFlexGap
            {...props}>
            <MonkeyHeadSvg className={classes.logo} color={color} />
            <MonkeNameSvg className={classes.name} color={color} />
        </Stack>
    );
};

export default MonkeyLogo;
