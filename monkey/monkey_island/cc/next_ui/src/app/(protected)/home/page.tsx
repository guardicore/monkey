'use client';
import { useGetAllMachinesQuery } from '@/redux/features/api/authentication/islandApi';

const HomePage = () => {
    const { data, isLoading } = useGetAllMachinesQuery();

    if (isLoading) return <div>loading...</div>;
    else return <div>{MachineList(data)}</div>;
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
