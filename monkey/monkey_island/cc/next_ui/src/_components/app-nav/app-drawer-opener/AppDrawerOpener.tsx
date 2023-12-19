import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import classes from './appDrawerOpener.module.scss';
import useSmallScreenCheck from '@/hooks/useSmallScreenCheck';

const AppDrawerOpener = ({ onClick }: { onClick: object }) => {
    const { screenIsSmall } = useSmallScreenCheck();

    const handleClick = () => {
        // @ts-ignore
        onClick();
    };

    if (!screenIsSmall) {
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
