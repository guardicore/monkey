import type { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import authPages from './authPages';
import { nanoid } from 'nanoid';
import { HTTP_METHODS } from '@/constants/http.constants';

export const authOptions: NextAuthOptions = {
    providers: [
        CredentialsProvider({
            name: 'Credentials',
            credentials: {},
            async authorize(credentials) {
                const { username, password } = credentials as any;
                let resBody: any = null;

                if (!username || !password) {
                    return null;
                }

                // This is where you need to retrieve user data
                // to verify with credentials
                // Docs: https://next-auth.js.org/configuration/providers/credentials
                try {
                    const loginResponse = await fetch(
                        `${process.env.BASE_API}/login`,
                        {
                            method: HTTP_METHODS.POST,
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            // @ts-ignore
                            body: JSON.stringify({ username, password })
                        }
                    );
                    resBody = await loginResponse.json();
                } catch (e) {
                    return null;
                }

                if (!resBody) {
                    return null;
                }

                const statusCode = resBody?.meta?.code;

                if (statusCode !== 200) {
                    return null;
                }
                const user = resBody?.response?.user;

                if (user) {
                    return user;
                } else {
                    return null;
                }
            }
        })
    ],
    callbacks: {
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        async signIn({ user, account, profile, email, credentials }: any) {
            if (user && user?.authentication_token) {
                return true;
            }
            return false;
        },
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        async jwt({ token, user, account, profile, isNewUser }: any) {
            // Add access_token to the token right after signin
            if (user) {
                const secondsToExpire = Math.floor(
                    Date.now() / 1000 + user.token_ttl_sec
                );
                return {
                    access_token: user.authentication_token,
                    expires_at: Math.floor(
                        Date.now() / 1000 + user.token_ttl_sec
                    ),
                    exp: secondsToExpire,
                    refresh_token: user.authentication_token
                };
            } else if (Date.now() < token.expires_at * 1000 - 200) {
                return token;
            } else {
                try {
                    let refreshTokenResponseBody = null;
                    if (token?.access_token) {
                        const options = {
                            method: HTTP_METHODS.POST,
                            headers: {
                                Accept: 'application/json',
                                'Content-Type': 'application/json',
                                'Authentication-Token': token.refresh_token
                            }
                        };

                        const refreshTokenResponse = await fetch(
                            `${process.env.BASE_API}/refresh-authentication-token`,
                            options
                        );
                        refreshTokenResponseBody =
                            await refreshTokenResponse.json();
                    }

                    if (!refreshTokenResponseBody) {
                        throw new Error('RefreshAccessTokenError');
                    }

                    if (refreshTokenResponseBody?.response?.errors) {
                        throw new Error(
                            JSON.stringify(
                                refreshTokenResponseBody?.response?.errors
                            )
                        );
                    }

                    const statusCode = refreshTokenResponseBody?.meta?.code;
                    if (statusCode && statusCode !== 200) {
                        throw new Error('RefreshAccessTokenError');
                    }

                    const newData = refreshTokenResponseBody?.response?.user;

                    if (!newData?.authentication_token) {
                        throw new Error('RefreshAccessTokenError');
                    }

                    const secondsToExpire = Math.floor(
                        Date.now() / 1000 + newData.token_ttl_sec
                    );

                    return {
                        ...token, // Keep the previous token properties
                        access_token: newData.authentication_token,
                        expires_at: secondsToExpire,
                        exp: secondsToExpire,
                        // Fall back to old refresh token
                        refresh_token: newData.authentication_token
                    };
                } catch (error) {
                    console.error('Error refreshing access token', error);

                    return null; // clear the session if the refresh token gets an error

                    // The error property will be used client-side to handle the refresh token error
                    // return {
                    //     ...token,
                    //     error: 'RefreshAccessTokenError' as const
                    // };
                }
            }
        },
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        async session({ session, user, token }: any) {
            if (token.error) {
                session.error = token.error;
            } else {
                session.accessToken = token.access_token;
                session.user.id = token.id || nanoid();
            }
            return session;
        }
    },
    session: {
        strategy: 'jwt',
        maxAge: 900 // 15 minutes
    },
    secret: process.env.NEXTAUTH_SECRET,
    pages: authPages
};
