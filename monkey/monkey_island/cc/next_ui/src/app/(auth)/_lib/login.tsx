import { HTTP_METHODS } from '@/constants/http.constants';
import { setToken } from '@/_lib/authentication';

type LoginValues = {
    username: string;
    password: string;
};

export const login = async (loginValues: LoginValues) => {
    const loginResponse = await fetch(`/api/login`, {
        method: HTTP_METHODS.POST,
        headers: {
            'Content-Type': 'application/json'
        },
        // @ts-ignore
        body: JSON.stringify(loginValues)
    });

    if (loginResponse.status !== 200) {
        return null;
    }

    const resBody = await loginResponse.json();

    const token = resBody?.response?.user?.authentication_token;
    const ttl = resBody?.response?.user?.token_ttl_sec * 1000;

    if (!token) {
        return null;
    } else {
        setToken(token, ttl);
    }
};
