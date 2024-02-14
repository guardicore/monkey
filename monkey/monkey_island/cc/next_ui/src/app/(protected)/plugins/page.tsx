'use client';
import { useGetAvailablePluginsQuery } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import React from 'react';
import PluginSidebar from '@/app/(protected)/plugins/pluginSidebar';
import Grid from '@mui/material/Unstable_Grid2';

export default function Plugins() {
    const { data, error, isLoading, isError, isSuccess } =
        useGetAvailablePluginsQuery();

    let content: null | React.ReactNode = null;

    if (isSuccess) content = <div>{JSON.stringify(data)}</div>;
    else if (isLoading) content = <div>loading...</div>;
    else if (isError) content = <div>Error: {error.data.response.errors}</div>;
    return (
        <Grid container spacing={5}>
            <Grid xs={3}>
                <PluginSidebar />
            </Grid>
            <Grid xs>{content}</Grid>
        </Grid>
    );
}
