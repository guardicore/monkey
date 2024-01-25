'use client';
import { injectProperties } from '@/utils/common/injection.utils';
import IAuthenticationRepository from '@/repositories/IAuthenticationRepository';
import SignInPage from './SignInPage';

export const buildSignInPage = (
    authenticationRepository: IAuthenticationRepository
) => injectProperties(SignInPage, { authenticationRepository });

export default buildSignInPage;
