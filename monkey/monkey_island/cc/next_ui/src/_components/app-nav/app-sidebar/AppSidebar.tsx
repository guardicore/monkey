import React from 'react';
import Paper from '@mui/material/Paper';
import MenuList from '@mui/material/MenuList';
import Divider from '@mui/material/Divider';
import { SidebarStyle } from '@/_components/app-nav/app-sidebar/style';

type sidebarProps = {
    items: React.JSX.Element[];
};

export default function AppSidebar(props: sidebarProps) {
    const displayItems: React.JSX.Element[] = [];
    for (let i = 0; i < props.items.length; i++) {
        if (props.items[i].props.prependDivider) {
            displayItems.push(<Divider key={`sidebar-divider-${i}`} />);
        }
        displayItems.push(props.items[i]);
    }
    return (
        <Paper sx={SidebarStyle}>
            <MenuList>{displayItems}</MenuList>
        </Paper>
    );
}
