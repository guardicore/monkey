import { NextRequest, NextResponse } from 'next/server';
// import { HTTP_METHODS } from '@/constants/http.constants';
import signup_success from '../../../../../mocks/auth/signup/signup_success.json';
// import signup_error from '../../../../../mocks/auth/signup/signup_error.json';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const POST = async (req: NextRequest) => {
    // @ts-ignore
    try {
        try {
            // const requestBody = await req.json();
            // TODO: register call
            // const registerResponse: any = await fetch(
            //     `${process.env.NEXT_PUBLIC_EXTERNAL_API_BASE_URL}/register`,
            //     {
            //         method: HTTP_METHODS.POST,
            //         headers: {
            //             'Content-Type': 'application/json'
            //         },
            //         body: requestBody
            //     }
            // );
        } catch (e) {
            return getErrorResponse('Error on sign up');
        }

        const registerResponse: any = signup_success;
        if (registerResponse?.meta?.code === 200) {
            return NextResponse.json('Successfully signed up', {
                status: 200
            });
        }

        return getErrorResponse(registerResponse?.response?.field_errors);
    } catch (error) {
        return getErrorResponse(error);
    }
};

const getErrorResponse = (error: any) => {
    return NextResponse.json(error, { status: 400 });
};
