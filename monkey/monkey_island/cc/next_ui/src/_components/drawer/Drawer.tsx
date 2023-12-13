import Drawer from '@mui/material/Drawer';

export enum DrawerVariant {
    PERMANENT = 'permanent',
    PERSISTENT = 'persistent',
    TEMPORARY = 'temporary'
}

export enum DrawerAnchor {
    LEFT = 'left',
    RIGHT = 'right',
    TOP = 'top',
    BOTTOM = 'bottom'
}

const MonkeyDrawer = (props) => {
    const {
        children = null,
        variant = DrawerVariant.TEMPORARY,
        anchor = DrawerAnchor.LEFT,
        hideBackdrop = false,
        open = false,
        onClose = null,
        classes = null,
        ...rest
    } = props;

    return (
        <Drawer
            anchor={anchor}
            open={open}
            onClose={onClose}
            classes={classes}
            hideBackdrop={hideBackdrop}
            variant={variant}
            {...rest}>
            {children}
        </Drawer>
    );
};

export default MonkeyDrawer;
