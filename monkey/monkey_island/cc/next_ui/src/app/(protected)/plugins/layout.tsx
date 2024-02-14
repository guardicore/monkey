'use client';
import React from 'react';
import PluginSidebar from '@/app/(protected)/plugins/pluginSidebar';
import Grid from '@mui/material/Unstable_Grid2';

export default function Plugins({ children }: { children: React.ReactNode }) {
    return (
        <Grid container spacing={5}>
            <Grid xs={3}>
                <PluginSidebar />
            </Grid>
            <Grid xs>{children}</Grid>
        </Grid>
    );
}
