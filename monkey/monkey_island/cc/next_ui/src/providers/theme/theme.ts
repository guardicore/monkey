import { Roboto } from 'next/font/google';

export enum THEME_APPEARANCE {
    DARK_MODE = 'dark',
    LIGHT_MODE = 'light'
}

const roboto = Roboto({
    weight: ['300', '400', '500', '700'],
    subsets: ['latin'],
    display: 'swap'
});

const themeOptions = {
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
    },
    components: {}
};

export default themeOptions;
