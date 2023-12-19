import MonkeyDrawer, { DrawerVariant } from '@/_components/drawer/Drawer';
import AppMenu from '@/_components/app-nav/app-menu/AppMenu';
import useResponsive from '@/hooks/useResponsive';
import DrawerHeader from '@/_components/app-nav/app-drawer/drawer-header/DrawerHeader';

export interface AppDrawerProps {
    open: boolean;
    onClose?: () => void;
}

const AppDrawer = ({ open, onClose }: AppDrawerProps) => {
    const { matches } = useResponsive();

    if (!matches) {
        return null;
    }

    return (
        <MonkeyDrawer
            open={open}
            onClose={onClose}
            variant={DrawerVariant.TEMPORARY}
            PaperProps={{ className: 'app-drawer-paper' }}>
            <DrawerHeader onClose={onClose} />
            <AppMenu onClose={onClose} />
        </MonkeyDrawer>
    );
};

export default AppDrawer;
