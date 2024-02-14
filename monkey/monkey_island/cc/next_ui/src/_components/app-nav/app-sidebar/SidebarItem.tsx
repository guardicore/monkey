import React from 'react';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import { MenuItemProps } from '@mui/base';

type SidebarItemProps = MenuItemProps & {
    name: string;
    onClick?: () => void;
    icon?: React.ReactNode | null;
    rightContent?: React.ReactNode | null;
    selected?: boolean;
    // Used by AppSidebar to add a divider before this item
    prependDivider?: boolean;
};

const SidebarItem = (props: SidebarItemProps) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { prependDivider, name, icon, rightContent, onClick, ...rest } =
        props;
    return (
        <MenuItem onClick={onClick} {...rest}>
            <ListItemIcon>{icon}</ListItemIcon>
            <ListItemText>{name}</ListItemText>
            {rightContent}
        </MenuItem>
    );
};

export default SidebarItem;
