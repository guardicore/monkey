import React from 'react';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';

type SidebarItemProps = {
    name: string;
    onClick?: () => void;
    icon?: React.ReactNode | null;
    rightContent?: React.ReactNode | null;
    // This is used by the Sidebar component
    prependDivider?: boolean;
};

const SidebarItem = (props: SidebarItemProps) => {
    const { name, icon, rightContent, onClick } = props;
    return (
        <MenuItem onClick={onClick}>
            <ListItemIcon>{icon}</ListItemIcon>
            <ListItemText>{name}</ListItemText>
            {rightContent}
        </MenuItem>
    );
};

export default SidebarItem;
