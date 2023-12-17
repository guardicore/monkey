import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import classes from './appDrawerOpener.module.scss';
import useResponsive from '@/hooks/useResponsive';

const AppDrawerOpener = ({ onClick }) => {
    const { matches } = useResponsive();

    const handleClick = () => {
        onClick();
    };

    if (!matches) {
        return null;
    }

    return (
        <IconButton
            id={classes['app-drawer-opener']}
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={handleClick}>
            <MenuIcon />
        </IconButton>
    );
};

export default AppDrawerOpener;
