import { withAuth } from 'next-auth/middleware';
import authPages from '@/app/api/auth/[...nextauth]/authPages';
import { getToken } from 'next-auth/jwt';
import { NextResponse } from 'next/server';
import { AUTH_PATHS, AUTHENTICATED_PATHS } from '@/constants/paths.constants';

const PROTECTED_PATHS_FOR_AUTHORIZED_USER: string[] = [
    AUTH_PATHS.SIGN_IN,
    AUTH_PATHS.SIGN_UP
];

const isPathProtectedForAuthorizedUser = (pathname: string) => {
    return PROTECTED_PATHS_FOR_AUTHORIZED_USER.some((path: string) =>
        pathname.startsWith(path)
    );
};

// NextResponse.next() - continue to next middleware
// https://nextjs.org/docs/app/api-reference/functions/next-response#next
// NextResponse.redirect() - redirect to a new location
export default async function middleware(req: any) {
    const isProduction =
        process.env.NODE_ENV === process.env.NEXT_PUBLIC_PRODUCTION_KEY;

    if (!isProduction) {
        return NextResponse.next();
    }

    const token = await getToken({ req });
    const isAuthenticated = !!token;
    const pathname = req.nextUrl.pathname;
    console.log('middleware', pathname, isAuthenticated);

    if (isAuthenticated && isPathProtectedForAuthorizedUser(pathname)) {
        return NextResponse.redirect(
            new URL(AUTHENTICATED_PATHS.ROOT, req.url)
        );
    }

    if (!isAuthenticated && pathname.startsWith(AUTH_PATHS.SIGN_UP)) {
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
