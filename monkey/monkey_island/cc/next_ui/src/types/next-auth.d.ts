import 'next-auth';
import 'next-auth/jwt';

declare module 'next-auth' {
    /**
     * Returned by `useSession`, `getSession` and received as a prop on the `SessionProvider` React Context
     */
    interface Session {
        error?: string;
        accessToken: string;
        user: {
            id: string;
        };
    }
}

declare module 'next-auth/jwt' {
    /** Returned by the `jwt` callback and `getToken`, when using JWT sessions */
    interface JWT {
        id?: string;
        access_token: string;
        expires_at: number;
        exp: number;
        refresh_token: string;
        error?: string;
    }
}
