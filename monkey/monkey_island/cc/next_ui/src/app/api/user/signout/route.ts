import { getServerSession } from 'next-auth';
import { authOptions } from '@/app/api/auth/[...nextauth]/authOptions';
import { NextResponse } from 'next/server';
import { HTTP_METHODS } from '@/constants/http.constants';

export const POST = async () => {
    try {
        const session: any = await getServerSession(authOptions);
        // @ts-ignore
        if (session && session?.accessToken) {
            const logoutResponse = await fetch(
                `${process.env.BASE_API}/logout`,
                {
                    method: HTTP_METHODS.POST,
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': session.accessToken
                    }
                }
            );

            const logoutResponseBody = await logoutResponse.json();
            console.log('logoutResponseBody', logoutResponseBody);
            if (logoutResponseBody?.meta?.code === 200) {
                return NextResponse.json('Logged out from auth provider', {
                    status: 200
                });
            }
            return getErrorResponse(JSON.stringify(logoutResponseBody));
        }
        return getErrorResponse('Error logging out. No session found.');
    } catch (error) {
        return getErrorResponse(error);
    }
};

const getErrorResponse = (error: any) => {
    console.log('getErrorResponse', error);
    return NextResponse.json(error, { status: 400 });
};
