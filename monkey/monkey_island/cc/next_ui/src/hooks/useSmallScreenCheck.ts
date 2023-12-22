import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';

const useSmallScreenCheck = () => {
    const theme = useTheme();
    const screenIsSmall = useMediaQuery(theme.breakpoints.down('sm'));

    return { screenIsSmall };
};

export default useSmallScreenCheck;
