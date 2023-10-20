'use client';
import {useDispatch, useSelector} from 'react-redux';
import {fetchMachines, machineById} from '@/features/machineSlice';
import {useEffect} from 'react';

export default function Machine({params}: { params: { id: string } }) {
    const dispatch = useDispatch()
    const machine = useSelector((state) => machineById(state, params.id))

    useEffect(() => {
        dispatch(fetchMachines())
    }, [])

    return (
        <div>
            Machine: <br/>
            <pre>{JSON.stringify(machine, null, 2)}</pre>
        </div>
    )
}
