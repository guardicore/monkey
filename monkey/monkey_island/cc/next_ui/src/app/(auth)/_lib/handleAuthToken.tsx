import { setToken } from '@/_lib/authentication';

const handleAuthToken = async (response) => {
    const token = response?.response?.user?.authentication_token;
    const ttl = response?.response?.user?.token_ttl_sec * 1000;

    if (!token) {
        return null;
    } else {
        setToken(token, ttl);
        return true;
    }
};

export default handleAuthToken;
