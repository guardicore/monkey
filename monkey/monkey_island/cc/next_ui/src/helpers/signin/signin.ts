import { signIn } from 'next-auth/react';

type LoginValues = {
    username: string;
    password: string;
};

export const login = async (loginValues: LoginValues) => {
    await signIn('credentials', {
        redirect: true,
        callbackUrl: '/',
        username: loginValues.username,
        password: loginValues.password
    });
};
