import { deepmerge } from '@mui/utils';
import { createTheme } from '@mui/material/styles';
import { roboto, THEME_APPEARANCE } from '@/providers/theme/theme';

export const themeOptions = {
    palette: {
        mode: THEME_APPEARANCE.DARK_MODE,
        primary: {
            main: '#FFCC00',
            light: '#FFCD38',
            dark: '#B28704',
            contrastText: '#000'
        },
        secondary: {
            main: '#F50057',
            light: '#F73378',
            dark: '#AB003C',
            contrastText: '#FFF'
        }
    },
    typography: {
        fontFamily: roboto.style.fontFamily
    },
    components: {}
};

const createAuthenticationTheme = (theme) =>
    createTheme({ ...theme, ...themeOptions });

export default createAuthenticationTheme;
