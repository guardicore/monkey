import React from 'react';
import Paper from '@mui/material/Paper';
import MenuList from '@mui/material/MenuList';
import Divider from '@mui/material/Divider';

type sidebarProps = {
    items: React.JSX.Element[];
};

export default function AppSidebar(props: sidebarProps) {
    const displayItems: React.JSX.Element[] = [];
    for (let i = 0; i < props.items.length; i++) {
        // @ts-ignore
        if (props.items[i].props.prependDivider) {
            displayItems.push(<Divider key={`sidebar-divider-${i}`} />);
        }
        displayItems.push(props.items[i]);
    }
    return (
        <Paper sx={{ width: '100%', height: '100%' }}>
            <MenuList>{displayItems}</MenuList>
        </Paper>
    );
}
