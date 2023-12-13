'use client';
import { IconButton } from '@mui/material';
import LightModeOutlinedIcon from '@mui/icons-material/LightModeOutlined';
import DarkModeOutlinedIcon from '@mui/icons-material/DarkModeOutlined';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '@/redux/store';
import { THEME_APPEARANCE } from '@/providers/theme/theme';
import { setThemeAppearance } from '@/redux/features/theme/theme.slice';
import classes from './themeMode.module.scss';

export const ThemeMode = () => {
    const dispatch: AppDispatch = useDispatch();
    const isThemeInDarkMode = useSelector(
        (state: RootState) =>
            state.theme.themeAppearance === THEME_APPEARANCE.DARK_MODE
    );

    const changeThemeAppearance = () => {
        dispatch(
            setThemeAppearance(
                isThemeInDarkMode
                    ? THEME_APPEARANCE.LIGHT_MODE
                    : THEME_APPEARANCE.DARK_MODE
            )
        );
    };

    const getClassNames = (): string => {
        const themeMode: string = isThemeInDarkMode
            ? THEME_APPEARANCE.DARK_MODE
            : THEME_APPEARANCE.LIGHT_MODE;
        return `${themeMode}-mode`;
    };

    return (
        <div id={classes['theme-mode']}>
            <IconButton
                className={`theme-mode-button ${getClassNames()}`}
                onClick={changeThemeAppearance}
                size="small">
                {isThemeInDarkMode ? (
                    <DarkModeOutlinedIcon />
                ) : (
                    <LightModeOutlinedIcon />
                )}
            </IconButton>
        </div>
    );
};
