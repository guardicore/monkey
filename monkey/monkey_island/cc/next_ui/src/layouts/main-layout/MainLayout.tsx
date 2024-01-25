'use client';

import classes from './mainLayout.module.scss';
import container from '@/lib/container';
import AppDrawer from '@/components/app-nav/app-drawer/appDrawer';
import React, { useState } from 'react';

const MonkeyAppBar = container.cradle.AppBar;

export default function MainLayout({
    children
}: {
    children: React.ReactNode;
}) {
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);

    const closeAppDrawer = () => {
        setIsDrawerOpen(false);
    };

    return (
        <main id={classes['main-layout']}>
            <div id="app-bar-wrapper">
                <MonkeyAppBar setIsDrawerOpen={setIsDrawerOpen} />
            </div>
            <AppDrawer open={isDrawerOpen} onClose={closeAppDrawer} />
            <main id="app-content-wrapper">{children}</main>
        </main>
    );
}
