import { setToken } from '@/_lib/authenticationToken';
import { SuccessfulAuthenticationResponse } from '@/redux/features/api/authentication/authenticationEndpoints';

// This coefficient is meant to reduce the TTL to account for network latency.
// Should be below 1
const networkLatencyCoefficient = 0.9;

const parseTTLFromResponse = (ttlSeconds: number): number => {
    // Default timescale in javascript is milliseconds
    const ttl = ttlSeconds * 1000;
    return ttl * networkLatencyCoefficient;
};

const handleAuthToken = (response: SuccessfulAuthenticationResponse) => {
    const token = response.authenticationToken;

    const ttl = parseTTLFromResponse(response.tokenTTLSeconds);
    return setToken(token, ttl);
};

export default handleAuthToken;
