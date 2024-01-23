import { setToken } from '@/_lib/authentication';

// This coefficient is meant to reduce the TTL to account for network latency.
// Should be below 1
const networkLatencyCoefficient = 0.9;

const parseTTLFromResponse = (response): number => {
    const ttlSeconds = response?.response?.user?.token_ttl_sec;
    // Default timescale in javascript is milliseconds
    const ttl = ttlSeconds * 1000;
    return ttl * networkLatencyCoefficient;
};

const handleAuthToken = async (response) => {
    const token = response?.response?.user?.authentication_token;
    const ttl = parseTTLFromResponse(response);

    if (!token) {
        return null;
    } else {
        await setToken(token, ttl);
        return true;
    }
};

export default handleAuthToken;
