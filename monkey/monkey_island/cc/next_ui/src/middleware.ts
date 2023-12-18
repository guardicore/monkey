import { withAuth } from 'next-auth/middleware';
import authPages from '@/app/api/auth/[...nextauth]/authPages';
import { getToken } from 'next-auth/jwt';
import { NextResponse } from 'next/server';
import { AUTHENTICATION_PATHS, ROUTES } from '@/constants/paths.constants';

const isPathProtectedForAuthorizedUser = (pathname: string) => {
    // if pathname starts with any of the paths in PROTECTED_PATHS_FOR_AUTHORIZED_USER
    // return true
    return AUTHENTICATION_PATHS.some((path: string) =>
        pathname.startsWith(path)
    );
};

export default async function middleware(req: any) {
    const token = await getToken({ req });
    const isAuthenticated = !!token;
    const pathname = req.nextUrl.pathname;
    console.log('middleware', pathname, isAuthenticated);

    if (isAuthenticated && isPathProtectedForAuthorizedUser(pathname)) {
        return NextResponse.redirect(new URL(ROUTES.ROOT, req.url));
    }

    if (!isAuthenticated && pathname.startsWith(ROUTES.SIGN_UP)) {
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
