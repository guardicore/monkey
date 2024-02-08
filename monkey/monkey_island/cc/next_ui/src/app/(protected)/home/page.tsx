'use client';
import { useGetAllMachinesQuery } from '@/redux/features/api/machinesEndpoints';

const HomePage = () => {
    const { data, error, isLoading, isError, isSuccess } =
        useGetAllMachinesQuery();

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
