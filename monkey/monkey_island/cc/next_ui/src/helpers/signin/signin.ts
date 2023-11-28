import { signIn } from 'next-auth/react';
import { AUTHENTICATED_PATHS } from '@/constants/paths.constants';

type LoginValues = {
    username: string;
    password: string;
};

export const login = async (loginValues: LoginValues) => {
    await signIn('credentials', {
        redirect: true,
        callbackUrl: AUTHENTICATED_PATHS.ROOT,
        username: loginValues.username,
        password: loginValues.password
    });
};
