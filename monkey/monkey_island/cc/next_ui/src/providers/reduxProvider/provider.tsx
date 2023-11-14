'use client';
import { store } from '@/redux/store';
import { Provider } from 'react-redux';
import { ReactNode } from 'react';

export function ReduxProvider({ children }: { children: ReactNode }) {
    return <Provider store={store}>{children}</Provider>;
}
