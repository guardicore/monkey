import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import useSmallScreenCheck from '@/hooks/useSmallScreenCheck';
import { appDrawerOpener } from '@/_components/app-nav/app-drawer-opener/style';

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
            sx={appDrawerOpener}
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={handleClick}>
            <MenuIcon />
        </IconButton>
    );
};

export default AppDrawerOpener;
