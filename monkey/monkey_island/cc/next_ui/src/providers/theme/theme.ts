// import { Roboto } from 'next/font/google';

export enum THEME_APPEARANCE {
    DARK_MODE = 'dark',
    LIGHT_MODE = 'light',
    SYSTEM_MODE = 'system'
}

// const roboto = Roboto({
//     weight: ['300', '400', '500', '700'],
//     subsets: ['latin'],
//     display: 'swap'
// });

const themeOptions = {
    palette: {
        mode: THEME_APPEARANCE.LIGHT_MODE
    },
    // typography: {
    //     fontFamily: roboto.style.fontFamily
    // },
    components: {}
};

export default themeOptions;
