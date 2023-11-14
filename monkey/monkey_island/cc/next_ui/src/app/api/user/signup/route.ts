import { NextRequest, NextResponse } from 'next/server';
import { HTTP_METHODS } from '@/constants/http.constants';

export const POST = async (req: NextRequest) => {
    // @ts-ignore
    try {
        const requestBody = await req.json();
        console.log('requestBody', requestBody);
        const registerResponse = await fetch(
            `${process.env.BASE_API}/register`,
            {
                method: HTTP_METHODS.POST,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            }
        );

        const registerResponseBody = await registerResponse.json();
        console.log('registerResponseBody', registerResponseBody);
        if (registerResponseBody?.meta?.code === 200) {
            return NextResponse.json('Successfully signed up', {
                status: 200
            });
        }

        return getErrorResponse(
            JSON.stringify(
                registerResponseBody?.errors ||
                    registerResponseBody?.response?.field_errors
            )
        );
    } catch (error) {
        return getErrorResponse(error);
    }
};

const getErrorResponse = (error: any) => {
    return NextResponse.json(error, { status: 400 });
};
