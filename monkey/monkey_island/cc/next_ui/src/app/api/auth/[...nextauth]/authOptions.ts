import type { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import * as login_success from '../../../../../mocks/auth/login/login_success.json';
import authPages from './authPages';
import { nanoid } from 'nanoid';

export const authOptions: NextAuthOptions = {
    providers: [
        CredentialsProvider({
            name: 'Credentials',
            credentials: {},
            // @ts-ignore
            async authorize(credentials) {
                const { username, password } = credentials as any;

                if (!username || !password) {
                    return null;
                }

                // TODO: Implement this
                // This is where you need to retrieve user data
                // to verify with credentials
                // Docs: https://next-auth.js.org/configuration/providers/credentials
                const res = login_success;
                // console.log(res);
                const statusCode = res?.meta?.code;
                if (statusCode !== 200) {
                    return null;
                }
                const user = res?.response?.user;

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
                    // TODO: Implement this
                    const res = login_success;
                    // console.log('new res', res);
                    const statusCode = res?.meta?.code;
                    if (statusCode !== 200) {
                        throw new Error('RefreshAccessTokenError');
                    }
                    const user = res?.response?.user;

                    if (!user?.authentication_token) {
                        throw new Error('RefreshAccessTokenError');
                    }

                    const secondsToExpire = Math.floor(
                        Date.now() / 1000 + user.token_ttl_sec
                    );

                    return {
                        ...token, // Keep the previous token properties
                        access_token: user.authentication_token,
                        expires_at: secondsToExpire,
                        exp: secondsToExpire,
                        // Fall back to old refresh token
                        refresh_token: user.authentication_token
                    };
                } catch (error) {
                    console.error('Error refreshing access token', error);
                    // The error property will be used client-side to handle the refresh token error
                    return {
                        ...token,
                        error: 'RefreshAccessTokenError' as const
                    };
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
            // console.log('session', session, user, token);
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
