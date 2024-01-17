'use client';
import { ReactNode, useEffect, useState } from 'react';

import { useIdleTimer } from 'react-idle-timer';
import { shouldRefreshToken } from '@/_lib/authentication';
import { useRefreshTokenMutation } from '@/redux/features/api/authentication/authenticationEndpoints';

const TIMEOUT = 1000 * 60 * 15; // 15 minutes
const PROMPT_THRESHOLD = 1000 * 60 * 1; // 1 minute

export function AuthRefresh({ children }: { children: ReactNode }) {
    const [refreshToken] = useRefreshTokenMutation();
    const [remaining, setRemaining] = useState(0);
    const [active, setActive] = useState(false);
    const refreshAuthentication = async () => {
        console.debug('refreshAuthentication');
        if (shouldRefreshToken(!isIdle())) {
            console.log('Refreshing the token');
            try {
                await refreshToken();
            } catch (e) {
                console.error('Error refreshing token', e);
            }
        }
    };
    const { isIdle, getRemainingTime } = useIdleTimer({
        timeout: TIMEOUT,
        onAction: refreshAuthentication,
        promptBeforeIdle: PROMPT_THRESHOLD,
        // Prompt could be used to show a modal to the user, but we're just going to attempt a refresh
        onPrompt: refreshAuthentication
    });

    useEffect(() => {
        const interval = setInterval(() => {
            setRemaining(Math.ceil(getRemainingTime() / 1000));
            setActive(!isIdle());
        }, 500);

        return () => {
            clearInterval(interval);
        };
    });

    return (
        <div>
            <div>
                {active
                    ? 'Status: Active ' + remaining
                    : 'Status: IDLE ' + remaining}
            </div>
            {children}
        </div>
    );
}
