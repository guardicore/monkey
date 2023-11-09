import { withAuth } from 'next-auth/middleware';
import authPages from '@/app/api/auth/[...nextauth]/authPages';
import { getToken } from 'next-auth/jwt';
import { NextResponse } from 'next/server';

const ROOT_PATH: string = '/';
const SIGNUP_PATH: string = '/signup';
const SIGNIN_PATH: string = '/signin';
const PROTECTED_PATHS_FOR_AUTHORIZED_USER: string[] = [
    SIGNIN_PATH,
    SIGNUP_PATH
];

const isPathProtectedForAuthorizedUser = (pathname: string) => {
    // if pathname starts with any of the paths in PROTECTED_PATHS_FOR_AUTHORIZED_USER
    // return true
    return PROTECTED_PATHS_FOR_AUTHORIZED_USER.some((path: string) =>
        pathname.startsWith(path)
    );
};

export default async function middleware(req: any) {
    const token = await getToken({ req });
    const isAuthenticated = !!token;
    const pathname = req.nextUrl.pathname;
    console.log('middleware', pathname, isAuthenticated);

    if (isAuthenticated && isPathProtectedForAuthorizedUser(pathname)) {
        return NextResponse.redirect(new URL(ROOT_PATH, req.url));
    }

    if (!isAuthenticated && pathname.startsWith(SIGNUP_PATH)) {
        // https://nextjs.org/docs/app/api-reference/functions/next-response#next
        return NextResponse.next();
    }

    return withAuth(req, {
        pages: authPages
    });
}

// Applies next-auth only to matching routes - can be regex
// Ref: https://nextjs.org/docs/app/building-your-application/routing/middleware#matcher
// Leave empty to apply to all routes
/*
 * Match all request paths except for the ones starting with:
 * - api (API routes)
 * - _next/static (static files)
 * - _next/image (image optimization files)
 * - favicon.ico (favicon file)
 * - robots.txt (robots file)
 */
export const config = {
    matcher: ['/((?!api|_next/static|_next/image|favicon.ico|robots.txt).*)']
};
