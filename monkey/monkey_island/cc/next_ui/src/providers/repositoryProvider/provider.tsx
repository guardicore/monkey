'use client';

import { ReactNode, createContext } from 'react';
import IAuthenticationRepository from '@/repositories/IAuthenticationRepository';
import RTKAuthenticationRepository from '@/repositories/RTKAuthenticationRepository';
import { store } from '@/redux/store';

type RepositoryContextType = {
    authenticationRepository: IAuthenticationRepository;
};
export const RepositoryContext = createContext<RepositoryContextType>(
    {} as RepositoryContextType
);

function createRepositories(): RepositoryContextType {
    const authenticationRepository = new RTKAuthenticationRepository(store);
    return { authenticationRepository };
}

export function RepositoryProvider({ children }: { children: ReactNode }) {
    return (
        <RepositoryContext.Provider value={createRepositories()}>
            {children}
        </RepositoryContext.Provider>
    );
}
