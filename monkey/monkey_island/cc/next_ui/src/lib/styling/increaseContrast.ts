import { darken, lighten } from '@mui/system';

const increaseContrast = (color, theme, times = 1) => {
    const tonalOffset = times * theme.palette.tonalOffset;
    if (theme.palette.mode === 'dark') {
        return lighten(color, tonalOffset);
    } else {
        return darken(color, tonalOffset);
    }
};

export default increaseContrast;
