import MonkeyHeadSvg from '@/assets/svg-components/MonkeyHead.svg';
import MonkeNameSvg from '@/assets/svg-components/MonkeyName.svg';
import Stack from '@mui/material/Stack';

import { monkeyLogo } from '@/_components/icons/monkey-logo/style';
import { useTheme } from '@mui/material/styles';

const MonkeyLogo = (props) => {
    const theme = useTheme();
    const color = props.color || theme.palette.primary.main;

    return (
        <Stack direction="row" useFlexGap sx={monkeyLogo} {...props}>
            <MonkeyHeadSvg className={'logo'} color={color} />
            <MonkeNameSvg className={'name'} color={color} />
        </Stack>
    );
};

export default MonkeyLogo;
