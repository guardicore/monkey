import { Roboto } from 'next/font/google';

export enum THEME_APPEARANCE {
    DARK_MODE = 'dark',
    LIGHT_MODE = 'light',
    SYSTEM_MODE = 'system'
}

export const roboto = Roboto({
    weight: ['300', '400', '500', '700'],
    subsets: ['latin'],
    display: 'swap'
});

const themeOptions = {
    palette: {
        mode: THEME_APPEARANCE.LIGHT_MODE,
        primary: {
            main: '#FFCC00',
            light: '#FFCD38',
            dark: '#B28704',
            contrastText: '#000'
        },
        secondary: {
            main: '#0F63A4',
            light: '#3F82B6',
            dark: '#0A4572',
            contrastText: '#FFF'
        }
    },
    typography: {
        fontFamily: roboto.style.fontFamily
    },
    components: {}
};

export default themeOptions;
