import { getServerSession } from 'next-auth';
import { authOptions } from '@/app/api/auth/[...nextauth]/authOptions';
import { NextResponse } from 'next/server';
// import { HTTP_METHODS } from '@/constants/http.constants';
// import logout_error from '../../../../../mocks/auth/logout/logout_error.json';
import logout_success from '../../../../../mocks/auth/logout/logout_success.json';

export const POST = async () => {
    try {
        const session: any = await getServerSession(authOptions);
        // @ts-ignore
        if (session && session?.accessToken) {
            // TODO: logout call
            let logoutResponse: any = null;
            try {
                // logoutResponse = await fetch(
                //     `${process.env.NEXT_PUBLIC_EXTERNAL_API_BASE_URL}/logout`,
                //     {
                //         method: HTTP_METHODS.POST,
                //         headers: {
                //             'Content-Type': 'application/json',
                //             'Authentication-Token': session.accessToken
                //         }
                //     }
                // );
                logoutResponse = logout_success;
            } catch (e) {
                return getErrorResponse('Error on sign out');
            }

            if (logoutResponse?.meta?.code === 200) {
                return NextResponse.json('Logged out from auth provider', {
                    status: 200
                });
            }
        }
        return getErrorResponse('Error logging out');
    } catch (error) {
        return getErrorResponse(error);
    }
};

const getErrorResponse = (error: any) => {
    return NextResponse.json(error, { status: 400 });
};
