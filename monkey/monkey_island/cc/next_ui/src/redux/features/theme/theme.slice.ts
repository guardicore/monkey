import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { THEME_APPEARANCE } from '@/providers/theme/theme';
import {
    executeIfWindowDefined,
    localStorageGetItem
} from '@/utils/common/localStorage.utils';

const THEME_APPEARANCE_KEY = 'theme_appearance';
const getThemeAppearance = () => {
    let savedThemeAppearance = null,
        userPrefersDark = false;

    savedThemeAppearance = localStorageGetItem(THEME_APPEARANCE_KEY);
    executeIfWindowDefined(() => {
        userPrefersDark = window.matchMedia(
            `(prefers-color-scheme: ${THEME_APPEARANCE.DARK_MODE})`
        ).matches;
    });

    return savedThemeAppearance
        ? savedThemeAppearance
        : userPrefersDark
          ? THEME_APPEARANCE.DARK_MODE
          : THEME_APPEARANCE.LIGHT_MODE;
};

const initialState = {
    themeAppearance: getThemeAppearance()
};

const themeSlice = createSlice({
    name: 'theme',
    initialState,
    reducers: {
        setThemeAppearance(state, action: PayloadAction<THEME_APPEARANCE>) {
            localStorage.setItem(THEME_APPEARANCE_KEY, action.payload);
            state.themeAppearance = action.payload;
        }
    }
});

export const { setThemeAppearance } = themeSlice.actions;
export default themeSlice.reducer;
