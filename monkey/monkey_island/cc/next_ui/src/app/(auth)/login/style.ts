import { Theme } from '@mui/system';
import increaseContrast from '@/lib/styling/increaseContrast';

export const cardStyle = (theme: Theme) => {
    return {
        padding: '1.5em',
        zIndex: 100,
        backgroundColor: increaseContrast(
            theme.palette.background.default,
            theme,
            0.3
        )
    };
};
