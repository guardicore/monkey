'use client';

import MonkeyAppBar from '@/_components/app-nav/app-bar/AppBar';
import AppDrawer from '@/_components/app-nav/app-drawer/appDrawer';
import React, { useState } from 'react';
import { styled } from '@mui/material/styles';
import { appContentWrapper, mainLayout } from './style';

export default function MainLayout({
    children
}: {
    children: React.ReactNode;
}) {
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);

    const closeAppDrawer = () => {
        setIsDrawerOpen(false);
    };

    // @ts-ignore
    const MainLayout = styled('main')(mainLayout);
    const AppContentWrapper = styled('main')(appContentWrapper);

    return (
        <MainLayout>
            <MonkeyAppBar setIsDrawerOpen={setIsDrawerOpen} />
            <AppDrawer open={isDrawerOpen} onClose={closeAppDrawer} />
            <AppContentWrapper>{children}</AppContentWrapper>
        </MainLayout>
    );
}
