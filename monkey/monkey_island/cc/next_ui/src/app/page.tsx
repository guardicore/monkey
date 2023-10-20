'use client'
import {useEffect, useState} from 'react';
import {useRouter} from 'next/navigation'
import {useDispatch, useSelector} from 'react-redux';
import {fetchMachines, selectMachines} from '@/features/machineSlice';
import Link from 'next/link';

export default function Home() {
    const machines = useSelector(selectMachines)
    const [machineView, setMachineView] = useState([])
    const dispatch = useDispatch()

    const router = useRouter()

    useEffect(() => {
        let machineViews = [];
        for (let i = 0; i < machines.length; i++) {
            machineViews.push(
                <Link href={`/machine/${machines[i].id}`} key={machines[i].id}>
                    {machines[i].network_interfaces[0]}
                </Link>)
        }
        setMachineView(machineViews)
    }, [machines])

    useEffect(() => {
        dispatch(fetchMachines())
    }, [])

    if (typeof window !== 'undefined' && !localStorage.getItem('authentication_token')) {
        fetch('/api/registration-status', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        }).then((response) => {
            response.json().then((data) => {
                if (data.needs_registration) {
                    router.push('/register')
                } else {
                    router.push('/login')
                }
            })
        })
    }

    return (
        <div>
            <h2>Hello!</h2>
            <h3>Machines:</h3>
            {machineView}
        </div>
    )
}
