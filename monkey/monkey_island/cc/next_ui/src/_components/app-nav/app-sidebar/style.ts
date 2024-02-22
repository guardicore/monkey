import { Theme } from '@mui/system';

export const MenuItemStyle = (theme: Theme) => {
    return {
        height: '50px',
        '&.Mui-selected': {
            color: 'secondary.main',
            backgroundColor: 'unset',
            fontWeight: 'bold',
            svg: {
                fill: theme.palette.secondary.main
            }
        },
        '&.Mui-selected:hover': {
            backgroundColor: theme.palette.action.hover
        }
    };
};

export const SidebarStyle = {
    width: '100%',
    height: '100%',
    minWidth: '50px'
};
