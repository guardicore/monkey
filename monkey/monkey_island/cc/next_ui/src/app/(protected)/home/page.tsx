'use client';
import { useRouter } from 'next/navigation';
import { useGetAllMachinesQuery } from '@/redux/features/api/machinesEndpoints';
import { useEffect } from 'react';

const HomePage = () => {
    const router = useRouter();
    const { data, error, isLoading, isError, isSuccess } =
        useGetAllMachinesQuery();

    useEffect(() => {
        if (isError && error.status === 401) {
            router.push('/signin'); // redirect to login page
        }
    }, [isError, error, router]);

    if (isSuccess) return <div>{MachineList(data)}</div>;
    if (isLoading) return <div>loading...</div>;
    if (isError) {
        return <div>Error: {error.data.response.errors}</div>;
    }
};

const MachineList = (machines) => {
    return (
        <ul>
            {machines.map((machine) => (
                <li key={machine.id}>{machine.hostname}</li>
            ))}
        </ul>
    );
};

export default HomePage;
