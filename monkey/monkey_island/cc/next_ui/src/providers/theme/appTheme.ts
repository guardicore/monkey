import { Roboto } from 'next/font/google';
import { createTheme, ThemeOptions } from '@mui/material/styles';

export enum THEME_APPEARANCE {
    DARK_MODE = 'dark',
    LIGHT_MODE = 'light'
}

const roboto = Roboto({
    weight: ['300', '400', '500', '700'],
    subsets: ['latin'],
    display: 'swap'
});

const themeOptions: ThemeOptions = {
    palette: {
        mode: THEME_APPEARANCE.DARK_MODE,
        primary: {
            main: '#FFCC00'
        },
        secondary: {
            main: '#8976ff'
        }
    },
    typography: {
        fontFamily: roboto.style.fontFamily
    }
};

const appTheme = createTheme(themeOptions);

export default appTheme;
