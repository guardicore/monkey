import Drawer, { DrawerProps } from '@mui/material/Drawer';
import React from 'react';

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

export interface MonkeyDrawerProps extends DrawerProps {
    children?: React.ReactNode;
    variant?: DrawerVariant;
    anchor?: DrawerAnchor;
    hideBackdrop?: boolean;
    open?: boolean;
    onClose?: () => void;
}

const MonkeyDrawer = (props: MonkeyDrawerProps) => {
    const {
        children = null,
        variant = DrawerVariant.TEMPORARY,
        anchor = DrawerAnchor.LEFT,
        hideBackdrop = false,
        open = false,
        onClose = undefined,
        ...rest
    } = props;

    return (
        <Drawer
            anchor={anchor}
            open={open}
            onClose={onClose}
            hideBackdrop={hideBackdrop}
            variant={variant}
            {...rest}>
            {children}
        </Drawer>
    );
};

export default MonkeyDrawer;
