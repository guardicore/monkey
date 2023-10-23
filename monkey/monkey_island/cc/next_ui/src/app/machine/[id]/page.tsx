'use client';
import {useMemo} from 'react';
import {useGetAllMachinesQuery} from '@/fetching/islandApiSlice';
import {createSelector} from 'reselect';
import MachineView from '@/components/machineView';


export default function Machine({params}: { params: { id: string } }) {
    const theId = params.id

    const getSpecificMachine = useMemo(() => {
        const emptyObject = {}
        return createSelector(
            res => res.data,
            (res, machineId) => machineId,
            (data, machineId) => {
                return data?.find(machine => Number(machine.id) === Number(machineId)) ?? emptyObject
            }
        )
    }, [])

    const {specificMachine} = useGetAllMachinesQuery(undefined, {
        pollingInterval: 3000,
        selectFromResult: result => ({
            specificMachine: getSpecificMachine(result, theId)
        })
    })

    return (
        <div>
            Machine: <br/>
            {specificMachine === undefined ? <p>Loading...</p> : <MachineView machine={specificMachine}/>}
        </div>
    )
}
