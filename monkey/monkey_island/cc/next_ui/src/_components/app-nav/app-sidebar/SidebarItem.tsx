import React from 'react';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import { MenuItemProps } from '@mui/base';
import Typography from '@mui/material/Typography';
import { MenuItemStyle } from '@/_components/app-nav/app-sidebar/style';
import { useTheme } from '@mui/material/styles';

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
    const theme = useTheme();
    return (
        <MenuItem onClick={onClick} {...rest} sx={MenuItemStyle(theme)}>
            <ListItemIcon>{icon}</ListItemIcon>
            <ListItemText>
                <Typography noWrap> {name} </Typography>
            </ListItemText>
            {rightContent}
        </MenuItem>
    );
};

export default SidebarItem;
