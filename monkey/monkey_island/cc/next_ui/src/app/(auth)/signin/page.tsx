'use client';
import container from '@/lib/container';
import buildSignInPage from './builder';

const PageSignInPage = buildSignInPage(
    container.cradle.authenticationRepository
);

export default PageSignInPage;
