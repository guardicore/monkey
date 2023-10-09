'use client'
import LoginPage from '@/components/login/Login';
import authFetch from '@/utils/common/authFetch';
import {useEffect, useState} from 'react';
import Link from 'next/link'

export default function Home() {
    if (typeof window !== 'undefined' && !localStorage.getItem('authentication_token')) {
        return <LoginPage/>;
    }

    const [events, setEvents] = useState([]);
    const [eventsView, setEventsView] = useState([]);

    useEffect(() => {
        authFetch('/api/agent-events').then((response) => {
            response.json().then((data) => {
                setEvents(data);
            });
        });
    }, [])

    useEffect(() => {
        let eventsListView = [];
        for(let i = 0; i < events.length; i++) {
           eventsListView.push(
               <div><Link href={`/event/${events[i].id}`}>{events[i].id}</Link><br/></div>
           )
        }
        setEventsView(eventsListView);
    }, [events])



    return (
        <div>
            <h2>Hello!</h2>
            <h3>Events:</h3>
            {eventsView.length > 0 ? eventsView : 'No events'}
        </div>
    )
}
