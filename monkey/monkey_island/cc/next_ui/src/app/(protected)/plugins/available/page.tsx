'use client';
import { useGetAvailablePluginsQuery } from '@/redux/features/api/agentPlugins/agentPluginEndpoints';
import React from 'react';

export default function AvailablePluginsPage() {
    const { data, error, isLoading, isError, isSuccess } =
        useGetAvailablePluginsQuery();

    let content: null | React.ReactNode = null;

    if (isSuccess) content = <div>{JSON.stringify(data)}</div>;
    else if (isLoading) content = <div>loading...</div>;
    else if (isError) content = <div>Error: {error.data.response.errors}</div>;
    return <div>{content}</div>;
}
