import AppIcon from '@/assets/svg-components/AppIconSvg';
import AppTitleSvg from '@/assets/svg-components/AppTitleSvg';
import Stack from '@mui/material/Stack';

import { brandHeader } from '@/_components/icons/monkey-logo/style';
import { useTheme } from '@mui/material/styles';

const BrandHeader = (props) => {
    const theme = useTheme();
    const color = props.color || theme.palette.primary.main;

    return (
        <Stack direction="row" useFlexGap sx={{ ...brandHeader, ...props.sx }}>
            <AppIcon color={color} className={'app-icon'} />
            <AppTitleSvg color={color} className={'app-title'} />
        </Stack>
    );
};

export default BrandHeader;
