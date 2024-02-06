import { useRouter } from 'next/navigation';
import { useRegistrationStatusQuery } from '@/redux/features/api/authentication/authenticationEndpoints';
import { useEffect } from 'react';
import { PATHS } from '@/constants/paths.constants';
import { tokenIsStored } from '@/lib/authenticationToken';

const useRedirectToLogin = () => {
    const router = useRouter();
    const { data: registrationStatus, isLoading: isRegistrationStatusLoading } =
        useRegistrationStatusQuery(null);

    useEffect(() => {
        if (
            !isRegistrationStatusLoading &&
            !registrationStatus?.registrationNeeded &&
            !tokenIsStored()
        ) {
            router.push(PATHS.LOGIN);
        }
    }, [isRegistrationStatusLoading, registrationStatus, router]);
};

export default useRedirectToLogin;
