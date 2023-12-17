'use client';
import { IconButton } from '@mui/material';
import LightModeOutlinedIcon from '@mui/icons-material/LightModeOutlined';
import DarkModeOutlinedIcon from '@mui/icons-material/DarkModeOutlined';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '@/redux/store';
import { THEME_APPEARANCE } from '@/providers/theme/theme';
import { setThemeAppearance } from '@/redux/features/theme/theme.slice';
import classes from './themeMode.module.scss';
import Box from '@mui/material/Box';
import Tooltip from '@mui/material/Tooltip';

const SWITCH_TEXT: string = 'Switch to';
const LIGHT_TOOLTIP: string = `${SWITCH_TEXT} Light Mode`;
const DARK_TOOLTIP: string = `${SWITCH_TEXT} Dark Mode`;

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
        <Box id={classes['theme-mode']}>
            <Tooltip title={isThemeInDarkMode ? LIGHT_TOOLTIP : DARK_TOOLTIP}>
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
            </Tooltip>
        </Box>
    );
};
