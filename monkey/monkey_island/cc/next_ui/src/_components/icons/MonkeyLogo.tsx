import MonkeyHeadSvg from '@/assets/svg-components/MonkeyHead.svg';
import MonkeNameSvg from '@/assets/svg-components/MonkeyName.svg';
import Stack from '@mui/material/Stack';

import classes from './MonkeyLogo.module.scss';
import { useTheme } from '@mui/material/styles';

const MonkeyLogo = (props) => {
    const theme = useTheme();

    return (
        <Stack
            className={classes.monkeyLogo}
            direction="row"
            useFlexGap
            style={{
                zIndex: 200,
                marginBottom: '25px'
            }}
            {...props}>
            <MonkeyHeadSvg
                className={classes.logo}
                color={theme.palette.primary.dark}
            />
            <MonkeNameSvg
                className={classes.name}
                color={theme.palette.primary.dark}
            />
        </Stack>
    );
};

export default MonkeyLogo;
