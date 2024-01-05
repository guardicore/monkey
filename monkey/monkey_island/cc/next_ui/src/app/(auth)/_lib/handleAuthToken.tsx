import { setToken } from '@/_lib/authentication';

const handleAuthToken = async (response: Response) => {
    const resBody = await response.json();

    const token = resBody?.response?.user?.authentication_token;
    const ttl = resBody?.response?.user?.token_ttl_sec * 1000;

    if (!token) {
        return null;
    } else {
        setToken(token, ttl);
        return true;
    }
};

export default handleAuthToken;
