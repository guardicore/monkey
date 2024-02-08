import { Theme } from '@mui/system';
import { appBarHeight } from '@/_components/app-nav/app-bar/style';

export const drawerHeader = (theme: Theme) => {
    return {
        display: 'flex',
        alignItems: 'center',
        backgroundColor: theme.palette.primary.main,
        color: theme.palette.primary.contrastText,
        justifyContent: 'space-between',
        height: appBarHeight,
        marginBottom: '1rem',
        boxShadow:
            '0 2px 4px -1px rgba(0, 0, 0, 0.2), 0 4px 5px 0 rgba(0, 0, 0, 0.14), 0 1px 10px 0 rgba(0, 0, 0, 0.12)'
    };
};

export const logoWrapper = {
    display: 'flex',
    flex: 1,
    justifyContent: 'center',
    '&:hover': {
        cursor: 'pointer'
    }
};

export const logoSize = '2.5rem';

export const logoIcon = {
    fontSize: logoSize,
    marginLeft: logoSize
};
