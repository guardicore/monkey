'use client';
import Link from 'next/link';
import { useGetAvailablePluginsQuery } from '@/redux/features/api/plugins/pluginsEndpoints';
import React from 'react';

export default function Plugins() {
    const { data, error, isLoading, isError, isSuccess } =
        useGetAvailablePluginsQuery();

    if (isSuccess) return <div>{JSON.stringify(data)}</div>;
    if (isLoading) return <div>loading...</div>;
    if (isError) {
        return <div>Error: {error.data.response.errors}</div>;
    }
    return (
        <div>
            <center>
                <h2>Plugins</h2>
                <Link href="/">Return Home</Link>
            </center>
        </div>
    );
}
